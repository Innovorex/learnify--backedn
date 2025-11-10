import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional
from services.model_config import (
    GARUDA_API_KEY,
    GARUDA_BASE_URL,
    GARUDA_MODEL,
    GARUDA_TIMEOUT,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    AI_TUTOR_FALLBACK_MODEL,
    OPENROUTER_TIMEOUT
)
from services.garuda_ai_service import GarudaAIService
from services.rag_retrieval_service_local import rag_retrieval_service_local as rag_retrieval_service
from services.vector_store_service import get_vector_store
from services.curriculum_data import CurriculumDataService
from services.ncert_content_service import NCERTContentService
from services.content_formatter import get_content_formatter

logger = logging.getLogger(__name__)

class AITutorOrchestrator:
    def __init__(self):
        # Primary: Garuda AI Service
        self.garuda_service = None
        if GARUDA_API_KEY:
            try:
                self.garuda_service = GarudaAIService(
                    api_key=GARUDA_API_KEY,
                    base_url=GARUDA_BASE_URL,
                    model=GARUDA_MODEL,
                    timeout=GARUDA_TIMEOUT
                )
                print(f"[AI TUTOR] Garuda AI initialized successfully")
            except Exception as e:
                print(f"[AI TUTOR] Failed to initialize Garuda AI: {e}")
        else:
            print(f"[AI TUTOR] Garuda AI not configured - will use OpenRouter only")

        # Fallback: OpenRouter API configuration
        self.openrouter_api_key = OPENROUTER_API_KEY
        self.openrouter_base_url = OPENROUTER_BASE_URL
        self.openrouter_model = AI_TUTOR_FALLBACK_MODEL
        self.openrouter_timeout = OPENROUTER_TIMEOUT

        # Curriculum service for real syllabus content
        self.curriculum_service = CurriculumDataService()

        # Store active sessions in memory
        self.active_sessions = {}

        # Track Garuda conversation IDs for session continuity
        self.garuda_conversations = {}

    async def start_session(
        self,
        session_id: int,
        teacher_id: int,
        topic_name: str,
        subject: str,
        grade: str,
        state: str,
        board: str,
        is_bed_qualified: bool,
        material_id: Optional[int] = None,
        material_filename: Optional[str] = None,
        db = None
    ) -> Dict:
        """Start a new AI Tutor session"""

        print(f"[AI TUTOR] Starting session {session_id} for teacher {teacher_id}")
        print(f"[AI TUTOR] Topic: {topic_name}, Subject: {subject}, Grade: {grade}")
        print(f"[AI TUTOR] Board: {board}, State: {state}")
        print(f"[AI TUTOR] B.Ed Qualified: {is_bed_qualified}")
        print(f"[AI TUTOR] Material ID: {material_id}, Filename: {material_filename}")
        print(f"[AI TUTOR] >>> IMPORTANT: Using uploaded material = {material_id is not None}")

        # Step 1: Fetch REAL syllabus and textbook content
        syllabus_content = ""
        syllabus_fetched = False
        textbook_content = ""
        textbook_fetched = False

        # Step 1A: Try to fetch extracted CBSE textbook content (if board is CBSE and db is available)
        # IMPORTANT: Only fetch CBSE content if NOT using uploaded material
        if db and board.upper() in ["CBSE", "NCERT"] and not material_id:
            try:
                print(f"[AI TUTOR] Fetching extracted CBSE textbook content for {grade} {subject} - {topic_name}...")
                ncert_service = NCERTContentService(db)

                # Try to convert grade to int
                try:
                    grade_num = int(grade.split('-')[0]) if '-' in str(grade) else int(grade)
                except:
                    grade_num = None

                if grade_num:
                    # Get available chapters for this grade and subject
                    available_chapters = ncert_service.get_available_chapters(grade_num, subject)

                    if available_chapters:
                        print(f"[AI TUTOR] Found {len(available_chapters)} chapters for Grade {grade_num} {subject}")

                        # Try to find EXACT matching chapter for the topic
                        topic_lower = topic_name.lower().strip()
                        best_match_chapter = None
                        best_match_score = 0

                        for chapter in available_chapters:
                            chapter_name_lower = chapter['chapter_name'].lower().strip()

                            # Exact match (highest priority)
                            if topic_lower == chapter_name_lower:
                                best_match_chapter = chapter
                                best_match_score = 100
                                break

                            # Topic is contained in chapter name
                            elif topic_lower in chapter_name_lower:
                                if len(topic_lower) / len(chapter_name_lower) > 0.5:  # Significant overlap
                                    if 80 > best_match_score:
                                        best_match_chapter = chapter
                                        best_match_score = 80

                            # Chapter name is contained in topic
                            elif chapter_name_lower in topic_lower:
                                if len(chapter_name_lower) / len(topic_lower) > 0.5:
                                    if 70 > best_match_score:
                                        best_match_chapter = chapter
                                        best_match_score = 70

                        if best_match_chapter:
                            # Get the EXACT chapter content matching the topic
                            print(f"[AI TUTOR] Found matching chapter: {best_match_chapter['chapter_name']} (match score: {best_match_score})")

                            # Try to get topic-specific content first
                            topic_content = ncert_service.get_topic_content(
                                grade=grade_num,
                                subject=subject,
                                chapter_name=best_match_chapter['chapter_name'],
                                topic_name=topic_name
                            )

                            # Always get FULL chapter content (no truncation)
                            chapter_data = ncert_service.get_chapter_content(
                                grade=grade_num,
                                subject=subject,
                                chapter_name=best_match_chapter['chapter_name']
                            )

                            if chapter_data:
                                # Use FULL cleaned content (no 8000 char limit!)
                                textbook_content = chapter_data['cleaned_content']
                                textbook_fetched = True
                                print(f"[AI TUTOR] ✅ Fetched {len(textbook_content)} chars of FULL chapter content")
                                print(f"[AI TUTOR] Chapter: {chapter_data['chapter_name']}, Key concepts: {len(chapter_data['key_concepts'])}")
                        else:
                            print(f"[AI TUTOR] ⚠️ No matching chapter found for topic '{topic_name}' in Grade {grade_num} {subject}")
            except Exception as e:
                print(f"[AI TUTOR] Failed to fetch textbook content: {e}")
                import traceback
                traceback.print_exc()

        # Step 1B: Fetch curriculum structure (syllabus outline)
        # IMPORTANT: Only fetch syllabus if NOT using uploaded material
        if not material_id:
            try:
                print(f"[AI TUTOR] Fetching curriculum structure for {board} {grade} {subject}...")
                curriculum_data = self.curriculum_service.get_curriculum_data(
                    board=board,
                    subject=subject,
                    grade=grade
                )

                if curriculum_data and "units" in curriculum_data:
                    # Find the topic in the curriculum
                    topic_lower = topic_name.lower()
                    for unit_name, unit_data in curriculum_data["units"].items():
                        if "topics" in unit_data:
                            for curriculum_topic in unit_data["topics"]:
                                if topic_lower in curriculum_topic.lower() or curriculum_topic.lower() in topic_lower:
                                    # Found matching topic!
                                    syllabus_content = (
                                        f"CURRICULUM STRUCTURE: {board} Grade {grade} {subject}\n"
                                        f"Unit: {unit_name} (Weightage: {unit_data.get('weightage', 'N/A')})\n"
                                        f"Topic: {curriculum_topic}\n"
                                        f"Related Topics in Unit: {', '.join(unit_data['topics'])}\n"
                                    )
                                    syllabus_fetched = True
                                    print(f"[AI TUTOR] Found topic '{curriculum_topic}' in {unit_name}")
                                    break
                        if syllabus_fetched:
                            break

                    # If not found in specific topic, provide general unit info
                    if not syllabus_fetched and curriculum_data["units"]:
                        first_unit = list(curriculum_data["units"].keys())[0]
                        syllabus_content = (
                            f"CURRICULUM STRUCTURE: {board} Grade {grade} {subject}\n"
                            f"Available Units: {', '.join(curriculum_data['units'].keys())}\n"
                            f"Your topic '{topic_name}' relates to these curriculum areas.\n"
                        )
                        syllabus_fetched = True
                        print(f"[AI TUTOR] Provided general curriculum context")

            except Exception as e:
                print(f"[AI TUTOR] Failed to fetch curriculum: {e}")
                syllabus_content = f"{subject} Grade {grade} - {topic_name}"
                syllabus_fetched = False

        # Step 2: Retrieve pedagogy content from IGNOU (reduced for natural flow)
        # IMPORTANT: Only fetch pedagogy if NOT using uploaded material
        pedagogy_chunks = []
        if not material_id:
            print(f"[AI TUTOR] Retrieving pedagogy content...")
            rag_result = rag_retrieval_service.retrieve_for_ai_tutor(
                teacher_question=f"How to teach {topic_name}",
                subject=subject,
                grade=grade,
                is_bed_qualified=is_bed_qualified,
                top_k=2  # Reduced from 5 to 2 for less pedagogy weight
            )
            pedagogy_chunks = rag_result["results"]
        else:
            print(f"[AI TUTOR] Skipping pedagogy - using uploaded material only")

        # Step 3: Retrieve from uploaded material (if provided)
        material_chunks = []
        material_source = None
        material_language = 'English'  # Default language
        if material_id:
            print(f"[AI TUTOR] ✅ Retrieving from uploaded material {material_id}...")
            material_chunks, material_source, material_language = await self._retrieve_from_material(
                material_id=material_id,
                topic=topic_name,
                material_filename=material_filename
            )
            print(f"[AI TUTOR] Retrieved result: {len(material_chunks)} chunks")
            if len(material_chunks) == 0:
                print(f"[AI TUTOR] ⚠️ WARNING: No material chunks retrieved! Check if material {material_id} exists and is vectorized.")
        else:
            print(f"[AI TUTOR] No material_id provided - not using uploaded material")

        # Step 4: Build context using ContentFormatter for structured responses
        formatter = get_content_formatter()

        if textbook_content:
            # Use CBSE textbook content with structured formatting
            print(f"[AI TUTOR] Using ContentFormatter for CBSE content ({len(textbook_content)} chars)")
            context = formatter.format_comprehensive_overview(
                raw_content=textbook_content,
                topic_name=topic_name,
                subject=subject,
                grade=str(grade)
            )
        elif material_chunks:
            # Use uploaded material with structured formatting
            print(f"[AI TUTOR] Using ContentFormatter for uploaded material ({len(material_chunks)} chunks)")
            print(f"[AI TUTOR] 🔍 DEBUG: First chunk sample: {str(material_chunks[0])[:200]}")

            # Merge material chunks into one text
            material_text = "\n\n".join([chunk.get('content', '') for chunk in material_chunks[:50]])

            print(f"[AI TUTOR] 🔍 DEBUG: material_text length = {len(material_text)} chars")
            print(f"[AI TUTOR] 🔍 DEBUG: material_text preview (first 300 chars):")
            print(f"[AI TUTOR] {material_text[:300]}")

            context = formatter.format_comprehensive_overview(
                raw_content=material_text,
                topic_name=topic_name,
                subject=subject,
                grade=str(grade),
                is_uploaded_material=True  # Use special material analysis format
            )

            print(f"[AI TUTOR] 🔍 DEBUG: Generated context length = {len(context)} chars")
            print(f"[AI TUTOR] 🔍 DEBUG: Context starts with:")
            print(f"[AI TUTOR] {context[:500]}")
            print(f"[AI TUTOR] Using uploaded material analysis format - will extract all topics from PDF")
        else:
            # Fallback to old method if no content available
            print(f"[AI TUTOR] No textbook/material content - using fallback context builder")
            context = self._build_context(
                topic_name=topic_name,
                subject=subject,
                grade=grade,
                syllabus_content=syllabus_content,
                pedagogy_chunks=pedagogy_chunks,
                material_chunks=material_chunks,
                material_filename=material_filename,
                is_bed_qualified=is_bed_qualified,
                material_language=material_language,
                textbook_content=textbook_content
            )

        # Step 5: Generate AI response
        print(f"[AI TUTOR] Generating response...")
        response, model_used = self._generate_response(context, session_id)

        # Step 6: Store session in memory with FULL material content for future queries
        self.active_sessions[session_id] = {
            "topic_name": topic_name,
            "subject": subject,
            "grade": grade,
            "board": board,
            "state": state,
            "is_bed_qualified": is_bed_qualified,
            "material_id": material_id,
            "material_filename": material_filename,
            "material_chunks": material_chunks,  # Store ALL material chunks
            "material_language": material_language,
            "textbook_content": textbook_content,  # Store textbook content for future reference
            "syllabus_content": syllabus_content,
            "messages": [
                {"role": "assistant", "content": response}
            ]
        }

        print(f"[AI TUTOR] ✅ Session {session_id} stored with {len(material_chunks)} material chunks")

        return {
            "session_id": session_id,
            "initial_message": response,
            "syllabus_fetched": syllabus_fetched,
            "source_type": "uploaded_material" if material_id else "curriculum",
            "material_filename": material_filename,
            "pedagogy_sources": [
                {
                    "module": chunk["module"],
                    "subject": chunk["subject"],
                    "file_name": chunk["file_name"],
                    "relevance": chunk["relevance"]
                }
                for chunk in pedagogy_chunks
            ],
            "material_sources": material_source if material_source else [],
            "model_used": model_used,
            "created_at": datetime.now().isoformat()
        }

    async def chat(
        self,
        session_id: int,
        user_message: str,
        subject: str,
        grade: str,
        is_bed_qualified: bool
    ) -> Dict:
        """Continue conversation in an active session with FULL material context"""

        print(f"[AI TUTOR] Chat in session {session_id} - Question: {user_message[:100]}...")

        # Get session data with stored material
        session = self.active_sessions.get(session_id, {})
        if not session:
            raise ValueError(f"Session {session_id} not found")

        conversation_history = session.get("messages", [])
        material_chunks = session.get("material_chunks", [])
        textbook_content = session.get("textbook_content", "")
        material_filename = session.get("material_filename")
        material_language = session.get("material_language", 'English')
        topic_name = session.get("topic_name", "")

        # Add user message to history
        conversation_history.append({"role": "user", "content": user_message})

        print(f"[AI TUTOR] Session has {len(material_chunks)} material chunks stored")
        print(f"[AI TUTOR] Textbook content: {'Yes' if textbook_content else 'No'}")

        # PERFORMANCE FIX: Extract only RELEVANT section of content for this question
        # Instead of sending ALL 40K+ chars, send only ~3-5K relevant chars
        relevant_content = ""

        if textbook_content:
            # Extract relevant portion from textbook content
            print(f"[AI TUTOR] Extracting relevant section from textbook ({len(textbook_content)} chars total)")
            relevant_content = self._extract_relevant_section(user_message, textbook_content, max_chars=5000)
            print(f"[AI TUTOR] Extracted {len(relevant_content)} chars of relevant content")
        elif material_chunks:
            # Extract relevant chunks from material
            print(f"[AI TUTOR] Finding relevant chunks from {len(material_chunks)} total chunks")
            relevant_chunks = self._find_relevant_chunks(user_message, material_chunks, max_chunks=5)
            relevant_content = "\n\n".join([f"[Page {c.get('page_number', 'N/A')}]\n{c.get('content', '')}"
                                           for c in relevant_chunks])
            print(f"[AI TUTOR] Selected {len(relevant_chunks)} relevant chunks ({len(relevant_content)} chars)")

        # Use ContentFormatter for follow-up prompts (much faster)
        formatter = get_content_formatter()
        context = formatter.format_followup_prompt(
            topic_name=topic_name,
            relevant_content=relevant_content,
            user_question=user_message,
            conversation_history=conversation_history,
            subject=session.get("subject", "General")
        )

        # Generate response
        response, model_used = self._generate_response(context, session_id)

        # Update conversation history
        conversation_history.append({"role": "assistant", "content": response})
        if session_id in self.active_sessions:
            self.active_sessions[session_id]["messages"] = conversation_history

        return {
            "session_id": session_id,
            "response": response,
            "additional_sources": [],  # No additional sources for follow-up questions
            "model_used": model_used,
            "timestamp": datetime.now().isoformat()
        }

    def _extract_relevant_section(self, question: str, full_content: str, max_chars: int = 5000) -> str:
        """
        Extract most relevant portion of content for the question.
        Uses simple keyword matching + context window.

        This is a PERFORMANCE optimization - instead of sending 40K chars to LLM,
        we send only ~3-5K most relevant chars.
        """
        question_lower = question.lower()
        question_words = set(question_lower.split())

        # Remove common words
        stop_words = {'what', 'is', 'the', 'a', 'an', 'how', 'why', 'when', 'where', 'can', 'you', 'explain', 'tell', 'me', 'about'}
        question_keywords = question_words - stop_words

        content_lines = full_content.split('\n')

        # Find lines containing question keywords
        scored_sections = []

        for i, line in enumerate(content_lines):
            line_lower = line.lower()
            # Score based on keyword matches
            score = sum(1 for keyword in question_keywords if keyword in line_lower)

            if score > 0:
                # Include context: 20 lines before and after
                start = max(0, i - 20)
                end = min(len(content_lines), i + 20)
                section = '\n'.join(content_lines[start:end])
                scored_sections.append((score, section))

        # If we found matches, return highest scoring section
        if scored_sections:
            scored_sections.sort(reverse=True, key=lambda x: x[0])
            relevant_text = scored_sections[0][1]
        else:
            # No keyword match - return first portion
            relevant_text = '\n'.join(content_lines[:100])

        # Truncate to max_chars
        return relevant_text[:max_chars]

    def _find_relevant_chunks(self, question: str, all_chunks: List[Dict], max_chunks: int = 5) -> List[Dict]:
        """
        Find most relevant chunks from material based on question.
        Uses simple keyword matching.

        Returns top N most relevant chunks instead of all 50.
        """
        question_lower = question.lower()
        question_words = set(question_lower.split())

        # Remove common words
        stop_words = {'what', 'is', 'the', 'a', 'an', 'how', 'why', 'when', 'where', 'can', 'you', 'explain', 'tell', 'me', 'about'}
        question_keywords = question_words - stop_words

        # Score each chunk
        scored_chunks = []
        for chunk in all_chunks:
            content = chunk.get('content', '').lower()
            score = sum(1 for keyword in question_keywords if keyword in content)
            if score > 0:
                scored_chunks.append((score, chunk))

        # If we found matches, return top N
        if scored_chunks:
            scored_chunks.sort(reverse=True, key=lambda x: x[0])
            return [chunk for score, chunk in scored_chunks[:max_chunks]]
        else:
            # No matches - return first few chunks
            return all_chunks[:max_chunks]

    def _build_context(
        self,
        topic_name: str,
        subject: str,
        grade: str,
        syllabus_content: str,
        pedagogy_chunks: List[Dict],
        material_chunks: List[Dict],
        material_filename: Optional[str],
        is_bed_qualified: bool,
        material_language: str = 'English',
        textbook_content: str = ""
    ) -> str:
        """Build context for Claude"""

        context_parts = [
            f"You are an AI Teaching Assistant helping a Grade {grade} {subject} teacher.\n",
            f"Topic: {topic_name}\n\n",
            "🌐 LANGUAGE: Always respond in ENGLISH, even if the material is in Hindi or Telugu.\n"
            "Translate and explain Hindi/Telugu content in English.\n\n"
        ]

        # Add curriculum structure (syllabus outline)
        if syllabus_content and len(syllabus_content) > 20:
            context_parts.append(
                f"📚 CURRICULUM STRUCTURE:\n"
                f"{syllabus_content}\n\n"
            )

        # Add extracted CBSE textbook content (if available) - THIS IS THE KEY CONTENT
        if textbook_content and len(textbook_content) > 50:
            context_parts.append(
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{textbook_content}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"⭐ CRITICAL: USE ONLY THIS TEXTBOOK CONTENT AS YOUR SOURCE.\n"
                f"✅ Answer ONLY based on this specific topic/chapter content.\n"
                f"❌ Do NOT provide information outside this content.\n"
                f"❌ Do NOT give general knowledge beyond this material.\n"
                f"Stay strictly focused on explaining what's in this content.\n\n"
            )

        # If uploaded material is provided, use it as primary source
        if material_chunks:
            context_parts.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            context_parts.append(f"📄 TEACHER'S UPLOADED MATERIAL (from: {material_filename})\n")
            context_parts.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")

            for chunk in material_chunks:
                page = chunk.get('page_number', 'N/A')
                content = chunk.get('content', '')
                context_parts.append(f"[Page {page}]\n{content}\n\n")

            context_parts.append(
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"⭐ CRITICAL: ANSWER ONLY BASED ON THIS UPLOADED MATERIAL.\n"
                f"✅ Explain concepts found in this material only.\n"
                f"❌ Do NOT add information not present in this material.\n"
                f"❌ Do NOT provide general knowledge beyond this content.\n"
                f"Stay strictly focused on what's in the uploaded material.\n\n"
            )

            # Different instructions based on B.Ed qualification
            if is_bed_qualified:
                # B.Ed teachers: Brief summary + DEEP concept explanation (NO teaching tips)
                context_parts.append(
                    f"You are helping a B.Ed/M.Ed qualified teacher deeply understand '{topic_name}' from the uploaded material.\n\n"

                    "YOUR PRIMARY GOAL: EXPLAIN THE CONCEPT THOROUGHLY AND CLEARLY.\n\n"

                    "STRUCTURE YOUR RESPONSE:\n\n"

                    "1. BRIEF OVERVIEW (5% - 2-3 sentences only):\n"
                    f"   - This material covers {topic_name} for Grade {grade} {subject}, pages X to Y\n"
                    "   - One sentence on what the concept is about\n\n"

                    "2. DEEP CONCEPT EXPLANATION (95% - THIS IS THE MAIN FOCUS):\n"
                    "   Your MAIN task is to explain the concept thoroughly:\n\n"

                    "   A. WHAT IS THE CONCEPT?\n"
                    "      - Define the concept in clear, precise language\n"
                    "      - If material is in Hindi/Telugu, translate key terms and explain in English\n"
                    "      - Reference specific page numbers (e.g., 'On page 5...')\n\n"

                    "   B. BREAK DOWN THE CONCEPT:\n"
                    "      - Explain each part/component of the concept step-by-step\n"
                    "      - Use analogies and real-world examples to make it crystal clear\n"
                    "      - Connect to what students already know\n\n"

                    "   C. EXAMPLES & APPLICATIONS:\n"
                    "      - Explain ALL examples from the material in detail\n"
                    "      - Show how formulas/theorems work with step-by-step walkthrough\n"
                    "      - Provide additional examples if needed for clarity\n\n"

                    "   D. COMMON MISCONCEPTIONS:\n"
                    "      - What do students typically misunderstand about this concept?\n"
                    "      - Clarify these confusions explicitly\n\n"

                    "   E. WHY THIS MATTERS:\n"
                    "      - Why is this concept important in {subject}?\n"
                    "      - How does it connect to other topics?\n\n"

                    "CRITICAL INSTRUCTIONS:\n"
                    "- 95% of your response should be explaining the CONCEPT itself\n"
                    "- Be thorough, clear, and detailed in your explanation\n"
                    "- Use simple English even when translating Hindi/Telugu material\n"
                    "- Do NOT include teaching tips (they have B.Ed training)\n"
                    "- Focus on UNDERSTANDING the concept deeply\n"
                )
            else:
                # Non-B.Ed teachers: Brief summary + DEEP concept explanation + Teaching tips at END
                context_parts.append(
                    f"You are helping a teacher WITHOUT B.Ed qualification understand and teach '{topic_name}' from the uploaded material.\n\n"

                    "YOUR PRIMARY GOAL: EXPLAIN THE CONCEPT THOROUGHLY AND CLEARLY.\n\n"

                    "STRUCTURE YOUR RESPONSE:\n\n"

                    "1. BRIEF OVERVIEW (5% - 2-3 sentences only):\n"
                    f"   - This material covers {topic_name} for Grade {grade} {subject}, pages X to Y\n"
                    "   - One sentence on what the concept is about\n\n"

                    "2. DEEP CONCEPT EXPLANATION (80% - THIS IS THE MAIN FOCUS):\n"
                    "   Your MAIN task is to explain the concept thoroughly in simple language:\n\n"

                    "   A. WHAT IS THE CONCEPT?\n"
                    "      - Define the concept in simple, clear language (avoid jargon)\n"
                    "      - If material is in Hindi/Telugu, translate and explain in English\n"
                    "      - Reference specific page numbers (e.g., 'On page 5...')\n\n"

                    "   B. BREAK DOWN THE CONCEPT:\n"
                    "      - Explain each part/component step-by-step\n"
                    "      - Use everyday analogies and real-world examples\n"
                    "      - Make it relatable to common experiences\n"
                    "      - Assume they're learning this concept for the first time\n\n"

                    "   C. EXAMPLES & APPLICATIONS:\n"
                    "      - Explain ALL examples from the material in detail\n"
                    "      - Walk through formulas/problems step-by-step\n"
                    "      - Show WHY each step is done (not just HOW)\n"
                    "      - Provide additional simple examples if needed\n\n"

                    "   D. COMMON STUDENT MISTAKES:\n"
                    "      - What do students typically misunderstand?\n"
                    "      - Clarify these confusions with examples\n\n"

                    "   E. WHY THIS MATTERS:\n"
                    "      - Why is this concept important for students to learn?\n"
                    "      - How does it connect to everyday life?\n\n"

                    "3. TEACHING TIPS (15% - AT THE VERY END):\n"
                    "   After fully explaining the concept, provide practical classroom tips:\n"
                    "   - How to introduce this concept to Grade {grade} students\n"
                    "   - One interactive activity to make it engaging\n"
                    "   - Tips for explaining it in simple terms\n"
                )

                # Add minimal practical pedagogy tips for non-B.Ed (only if available)
                if pedagogy_chunks:
                    context_parts.append("\n\nPractical Teaching Insights (use these briefly in your teaching tips section):\n")
                    for i, chunk in enumerate(pedagogy_chunks[:2], 1):  # Only 2 chunks, reduced from 3
                        practical_tip = chunk['content'][:200].strip()
                        context_parts.append(f"- {practical_tip}\n")
                    context_parts.append("\n")

                context_parts.append(
                    "\nCRITICAL INSTRUCTIONS:\n"
                    "- 80% of your response should be explaining the CONCEPT itself\n"
                    "- Be thorough, clear, and detailed in your explanation\n"
                    "- Use simple English even when translating Hindi/Telugu material\n"
                    "- Teaching tips come AT THE VERY END (only 15%)\n"
                    "- Focus on UNDERSTANDING the concept deeply first\n"
                    "- Be supportive and encouraging\n"
                    "- Reference page numbers throughout\n"
                )

        else:
            # Standard behavior without uploaded material
            if is_bed_qualified:
                context_parts.append(
                    f"You are helping a B.Ed/M.Ed qualified teacher understand '{topic_name}' for Grade {grade} {subject}.\n\n"

                    "YOUR PRIMARY GOAL: EXPLAIN THE CONCEPT THOROUGHLY.\n\n"

                    "Focus 100% on deep concept explanation:\n"
                    "- Define the concept clearly and precisely\n"
                    "- Break down all components step-by-step\n"
                    "- Explain the 'why' behind each part\n"
                    "- Use multiple examples to illustrate the concept\n"
                    "- Highlight common student misconceptions and clarify them\n"
                    "- Show real-world applications\n"
                    "- Connect to other related concepts in {subject}\n"
                    "- Do NOT include teaching tips (they have B.Ed training)\n\n"

                    "Be thorough, clear, and academic in your explanation.\n"
                )
            else:
                # NON-B.ED TEACHER: Focus on concept explanation + brief teaching tips
                context_parts.append(
                    f"You are helping a teacher WITHOUT B.Ed qualification understand and teach '{topic_name}' to Grade {grade} {subject} students.\n\n"

                    "YOUR PRIMARY GOAL: EXPLAIN THE CONCEPT THOROUGHLY IN SIMPLE LANGUAGE.\n\n"

                    "STRUCTURE (natural flowing response):\n\n"

                    "1. CONCEPT EXPLANATION (80% of response - THIS IS THE MAIN FOCUS):\n"
                    "   - What is this concept? Define it in simple, everyday language\n"
                    "   - Break it down step-by-step (assume they're learning it fresh)\n"
                    "   - Use analogies and real-world examples to make it crystal clear\n"
                    "   - Explain WHY each part matters\n"
                    "   - Walk through 3-4 examples in detail (show every step)\n"
                    "   - Clarify common misconceptions\n"
                    "   - Show real-world applications\n\n"

                    "2. TEACHING TIPS (20% - AT THE END):\n"
                    "   - How to introduce this to Grade {grade} students\n"
                    "   - One interactive activity to make it engaging\n"
                    "   - Common mistakes to watch for\n\n"

                    "CRITICAL: 80% should be explaining the concept itself, only 20% teaching tips.\n"
                )

            # Add minimal, practical pedagogy for non-B.Ed (only 2 short chunks)
            if pedagogy_chunks and not is_bed_qualified:
                context_parts.append("Practical Teaching Insights (keep brief in your response):\n")
                for i, chunk in enumerate(pedagogy_chunks[:2], 1):
                    # Extract only 150 chars for brevity
                    practical_tip = chunk['content'][:150].strip()
                    context_parts.append(f"- {practical_tip}\n")
                context_parts.append("\n")

            context_parts.append(
                f"Write your response as ONE continuous, natural explanation - NOT divided into 'Part 1', 'Part 2', etc.\n"
                f"Remember: 60% concept clarity + 30% examples + 10% teaching tips.\n"
                f"Be conversational, encouraging, and supportive. The teacher is learning this to teach their students.\n"
            )

        return "".join(context_parts)

    def _generate_response(self, context: str, session_id: Optional[int] = None) -> tuple:
        """
        Generate response using Garuda AI (primary) with OpenRouter fallback

        Returns:
            tuple: (response_text, model_used)
        """

        # Step 1: Try Garuda AI first (if configured)
        if self.garuda_service:
            try:
                print(f"[AI TUTOR] Attempting Garuda AI (Primary)...")

                # Get conversation ID for session continuity
                conversation_id = self.garuda_conversations.get(session_id)

                result = self.garuda_service.generate_response(
                    message=context,
                    conversation_id=conversation_id
                )

                # Store conversation_id for future messages in this session
                if session_id and result.get("conversation_id"):
                    self.garuda_conversations[session_id] = result["conversation_id"]
                    print(f"[AI TUTOR] Stored Garuda conversation_id for session {session_id}")

                response_text = result["response"]
                model_used = f"Garuda AI ({result.get('model', GARUDA_MODEL)})"

                print(f"[AI TUTOR] ✓ Garuda AI success - Generated {len(response_text)} characters")
                logger.info(f"[AI TUTOR] Garuda AI - Session: {session_id}, Tokens: {result.get('usage', {})}")

                return response_text, model_used

            except Exception as e:
                print(f"[AI TUTOR] ✗ Garuda AI failed: {str(e)}")
                logger.error(f"[AI TUTOR] Garuda AI error: {str(e)}")
                print(f"[AI TUTOR] Falling back to OpenRouter...")

        # Step 2: Fallback to OpenRouter
        return self._generate_response_openrouter(context)

    def _generate_response_openrouter(self, context: str) -> tuple:
        """
        Generate response using OpenRouter API (fallback)

        Returns:
            tuple: (response_text, model_used)
        """
        try:
            print(f"[AI TUTOR] Using OpenRouter (Fallback)...")

            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.openrouter_model,
                "messages": [
                    {"role": "user", "content": context}
                ],
                "max_tokens": 4000,
                "temperature": 0.7
            }

            response = requests.post(
                f"{self.openrouter_base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.openrouter_timeout
            )

            response.raise_for_status()
            result = response.json()

            response_text = result["choices"][0]["message"]["content"]
            model_used = f"OpenRouter ({self.openrouter_model})"

            print(f"[AI TUTOR] ✓ OpenRouter success - Generated {len(response_text)} characters")
            logger.info(f"[AI TUTOR] OpenRouter - Model: {self.openrouter_model}")

            return response_text, model_used

        except Exception as e:
            print(f"[AI TUTOR ERROR] OpenRouter also failed: {str(e)}")
            logger.error(f"[AI TUTOR] OpenRouter error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[AI TUTOR ERROR] Response: {e.response.text}")

            error_message = "I apologize, but I encountered an error. Please try again."
            return error_message, "Error"

    def _detect_language(self, text_chunks: List[str]) -> str:
        """
        Detect the primary language of the material content
        Returns: 'Hindi', 'Telugu', or 'English'
        """
        if not text_chunks:
            return 'English'

        # Combine first few chunks for detection
        sample_text = ' '.join(text_chunks[:3])[:500]

        # Count characters from different scripts
        devanagari_count = sum(1 for c in sample_text if '\u0900' <= c <= '\u097F')  # Hindi/Devanagari
        telugu_count = sum(1 for c in sample_text if '\u0C00' <= c <= '\u0C7F')      # Telugu

        total_chars = len([c for c in sample_text if c.isalpha()])

        if total_chars == 0:
            return 'English'

        # If more than 30% characters are in a specific script, use that language
        if devanagari_count / total_chars > 0.3:
            return 'Hindi'
        elif telugu_count / total_chars > 0.3:
            return 'Telugu'
        else:
            return 'English'

    async def _retrieve_from_material(
        self,
        material_id: int,
        topic: str,
        material_filename: Optional[str] = None,
        load_all: bool = True  # NEW: Load all chunks by default for full material understanding
    ) -> tuple:
        """
        Retrieve chunks from uploaded teaching material

        Args:
            material_id: ID of the uploaded material
            topic: Topic name for focused retrieval (used if load_all=False)
            material_filename: Original filename
            load_all: If True, loads ALL material chunks for complete understanding

        Returns: (material_chunks, material_source_info, detected_language)
        """
        try:
            vector_store = get_vector_store()
            collection_name = f"material_{material_id}"

            # Check if collection exists
            if not vector_store.collection_exists(collection_name):
                print(f"[AI TUTOR] Collection {collection_name} does not exist")
                return [], None, 'English'

            if load_all:
                # Load ALL chunks from material for complete understanding
                print(f"[AI TUTOR] Loading ALL chunks from material {material_id} for complete understanding...")
                print(f"[AI TUTOR] Collection name: {collection_name}")
                results = vector_store.get_all_chunks(collection_name)
                print(f"[AI TUTOR] Results type: {type(results)}, keys: {results.keys() if isinstance(results, dict) else 'N/A'}")
                doc_count = len(results.get('documents', [[]])[0]) if results and 'documents' in results else 0
                print(f"[AI TUTOR] Loaded {doc_count} total chunks")
                if doc_count == 0:
                    print(f"[AI TUTOR] ⚠️⚠️⚠️ WARNING: get_all_chunks returned 0 documents for {collection_name}!")
            else:
                # Search for relevant chunks based on topic (old behavior)
                print(f"[AI TUTOR] Searching for topic-relevant chunks: {topic}")
                results = vector_store.search_similar_chunks(
                    collection_name=collection_name,
                    query=topic,
                    n_results=10
                )

            # Format chunks for context
            material_chunks = []
            print(f"[AI TUTOR] 🔍 Processing results - documents structure: {type(results.get('documents'))}")

            if results and 'documents' in results:
                documents = results['documents']
                metadatas = results.get('metadatas', [])

                print(f"[AI TUTOR] 🔍 Documents length: {len(documents)}")
                print(f"[AI TUTOR] 🔍 First level type: {type(documents)}")

                # ChromaDB get_all_chunks returns {'documents': [[doc1, doc2, ...]], ...}
                # The first [0] gets the inner list
                if isinstance(documents, list) and len(documents) > 0:
                    doc_list = documents[0] if isinstance(documents[0], list) else documents
                    meta_list = metadatas[0] if (isinstance(metadatas, list) and len(metadatas) > 0 and isinstance(metadatas[0], list)) else metadatas

                    print(f"[AI TUTOR] 🔍 Processing {len(doc_list)} documents")

                    for idx, doc in enumerate(doc_list):
                        metadata = meta_list[idx] if idx < len(meta_list) else {}

                        # For load_all, distances might not exist (all chunks loaded without similarity scoring)
                        relevance = 1.0  # Default relevance for all chunks
                        if 'distances' in results and results['distances'] and len(results['distances'][0]) > idx:
                            relevance = 1 - results['distances'][0][idx]  # Convert distance to similarity

                        material_chunks.append({
                            'content': doc,
                            'page_number': metadata.get('page_number', 'N/A'),
                            'section_title': metadata.get('section_title', ''),
                            'relevance': relevance,
                            'chunk_index': idx  # Track original position
                        })

                    print(f"[AI TUTOR] 🔍 Successfully created {len(material_chunks)} material chunks")
                else:
                    print(f"[AI TUTOR] ⚠️ Documents structure unexpected: {documents[:50] if documents else 'empty'}")

            # Detect language from material content
            content_texts = [chunk['content'] for chunk in material_chunks]
            detected_language = self._detect_language(content_texts)
            print(f"[AI TUTOR] Detected material language: {detected_language}")

            # Prepare source info for response
            material_source = {
                'filename': material_filename,
                'chunks_retrieved': len(material_chunks),
                'pages': list(set([c['page_number'] for c in material_chunks if c['page_number'] != 'N/A']))
            }

            print(f"[AI TUTOR] Retrieved {len(material_chunks)} chunks from {material_filename}")
            return material_chunks, material_source, detected_language

        except Exception as e:
            print(f"[AI TUTOR ERROR] Failed to retrieve from material: {e}")
            return [], None, 'English'

    def clear_session(self, session_id: int):
        """Clear session from memory"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]

        # Also clear Garuda conversation ID
        if session_id in self.garuda_conversations:
            del self.garuda_conversations[session_id]

# Initialize orchestrator
ai_tutor_orchestrator = AITutorOrchestrator()
