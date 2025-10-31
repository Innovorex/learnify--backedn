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
        material_filename: Optional[str] = None
    ) -> Dict:
        """Start a new AI Tutor session"""

        print(f"[AI TUTOR] Starting session {session_id} for teacher {teacher_id}")
        print(f"[AI TUTOR] Topic: {topic_name}, Subject: {subject}, Grade: {grade}")
        print(f"[AI TUTOR] B.Ed Qualified: {is_bed_qualified}")
        print(f"[AI TUTOR] Material ID: {material_id}")

        # Step 1: Fetch REAL syllabus content from curriculum
        syllabus_content = ""
        syllabus_fetched = False

        try:
            print(f"[AI TUTOR] Fetching curriculum data for {board} {grade} {subject}...")
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
                                    f"CURRICULUM: {board} Grade {grade} {subject}\n"
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
                        f"CURRICULUM: {board} Grade {grade} {subject}\n"
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
        pedagogy_chunks = []
        print(f"[AI TUTOR] Retrieving pedagogy content...")
        rag_result = rag_retrieval_service.retrieve_for_ai_tutor(
            teacher_question=f"How to teach {topic_name}",
            subject=subject,
            grade=grade,
            is_bed_qualified=is_bed_qualified,
            top_k=2  # Reduced from 5 to 2 for less pedagogy weight
        )
        pedagogy_chunks = rag_result["results"]

        # Step 3: Retrieve from uploaded material (if provided)
        material_chunks = []
        material_source = None
        if material_id:
            print(f"[AI TUTOR] Retrieving from uploaded material {material_id}...")
            material_chunks, material_source = await self._retrieve_from_material(
                material_id=material_id,
                topic=topic_name,
                material_filename=material_filename
            )

        # Step 4: Build context
        context = self._build_context(
            topic_name=topic_name,
            subject=subject,
            grade=grade,
            syllabus_content=syllabus_content,
            pedagogy_chunks=pedagogy_chunks,
            material_chunks=material_chunks,
            material_filename=material_filename,
            is_bed_qualified=is_bed_qualified
        )

        # Step 5: Generate AI response
        print(f"[AI TUTOR] Generating response...")
        response, model_used = self._generate_response(context, session_id)

        # Step 6: Store session in memory
        self.active_sessions[session_id] = {
            "topic_name": topic_name,
            "subject": subject,
            "grade": grade,
            "is_bed_qualified": is_bed_qualified,
            "material_id": material_id,
            "material_filename": material_filename,
            "messages": [
                {"role": "assistant", "content": response}
            ]
        }

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
        """Continue conversation in an active session"""

        print(f"[AI TUTOR] Chat in session {session_id}")

        # Retrieve additional pedagogy if needed (reduced for natural flow)
        rag_result = rag_retrieval_service.retrieve_for_ai_tutor(
            teacher_question=user_message,
            subject=subject,
            grade=grade,
            is_bed_qualified=is_bed_qualified,
            top_k=2  # Reduced from 3 to 2 for less pedagogy weight
        )
        pedagogy_chunks = rag_result["results"]

        # Get conversation history
        session = self.active_sessions.get(session_id, {})
        conversation_history = session.get("messages", [])

        # Add user message
        conversation_history.append({"role": "user", "content": user_message})

        # Build context for follow-up
        context_parts = [f"Previous conversation:\n"]
        for msg in conversation_history[-4:]:  # Last 4 messages for context
            context_parts.append(f"{msg['role']}: {msg['content'][:200]}...\n")

        context_parts.append(f"\nTeacher's new question: {user_message}\n\n")

        # Add minimal pedagogy only if not B.Ed qualified
        if pedagogy_chunks and not is_bed_qualified:
            context_parts.append("Brief teaching insights (keep minimal):\n")
            for chunk in pedagogy_chunks[:2]:
                context_parts.append(f"- {chunk['content'][:150]}...\n")
            context_parts.append("\n")

        # Natural flow instructions
        context_parts.append(
            "Provide a natural, conversational response:\n"
            "- Focus on answering their specific question clearly\n"
            "- If it's about the concept: explain it simply with examples\n"
            "- If it's about teaching: give practical, brief tips\n"
            "- Keep it flowing and natural (not broken into parts)\n"
            "- Be supportive and encouraging\n"
        )

        context = "".join(context_parts)

        # Generate response
        response, model_used = self._generate_response(context, session_id)

        # Update conversation history
        conversation_history.append({"role": "assistant", "content": response})
        if session_id in self.active_sessions:
            self.active_sessions[session_id]["messages"] = conversation_history

        return {
            "session_id": session_id,
            "response": response,
            "additional_sources": [
                {
                    "module": chunk["module"],
                    "subject": chunk["subject"],
                    "file_name": chunk["file_name"],
                    "relevance": chunk["relevance"]
                }
                for chunk in pedagogy_chunks
            ],
            "model_used": model_used,
            "timestamp": datetime.now().isoformat()
        }

    def _build_context(
        self,
        topic_name: str,
        subject: str,
        grade: str,
        syllabus_content: str,
        pedagogy_chunks: List[Dict],
        material_chunks: List[Dict],
        material_filename: Optional[str],
        is_bed_qualified: bool
    ) -> str:
        """Build context for Claude"""

        context_parts = [
            f"You are an AI Teaching Assistant helping a Grade {grade} {subject} teacher.\n",
            f"Topic: {topic_name}\n\n"
        ]

        # Add curriculum content prominently
        if syllabus_content and len(syllabus_content) > 20:
            context_parts.append(
                f"📚 OFFICIAL CURRICULUM INFORMATION:\n"
                f"{syllabus_content}\n"
                f"Use this curriculum context to ensure your explanation aligns with the syllabus.\n\n"
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

            context_parts.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")

            context_parts.append(
                "PROVIDE A COMPREHENSIVE 4-PART RESPONSE:\n\n"
                "📖 PART 1: CONTENT EXPLANATION (From Uploaded Material)\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Read and explain the content about '{topic_name}' from the uploaded material above.\n"
                "Include:\n"
                "- Main concepts and definitions FROM THE MATERIAL\n"
                "- Examples given in the material (mention page numbers)\n"
                "- Formulas/theorems mentioned in the material\n"
                "- Reference specific pages (e.g., 'As shown on page 5...')\n\n"

                "📚 PART 2: KEY EXAMPLES FROM THE MATERIAL\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "List the examples found in the material with page references.\n\n"

                "👨‍🏫 PART 3: TEACHING STRATEGIES (B.Ed Pedagogy)\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "Based on the content in the material and B.Ed principles:\n"
            )

            if pedagogy_chunks:
                context_parts.append("\nPEDAGOGICAL GUIDANCE (IGNOU B.Ed):\n")
                for i, chunk in enumerate(pedagogy_chunks[:3], 1):
                    context_parts.append(f"{i}. {chunk['content'][:400]}...\n\n")

            context_parts.append(
                "Provide:\n"
                "1. How to introduce this topic (use the material's structure)\n"
                "2. Teaching sequence (follow the material's flow)\n"
                "3. How to use the examples from specific pages\n"
                "4. Activities based on the material\n"
                "5. Common misconceptions to address\n\n"

                "✅ PART 4: LESSON PLAN USING THE MATERIAL\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "Create a 45-minute lesson plan that uses this material:\n"
                "- Introduction (5 min): What to say using material's content\n"
                "- Main Teaching (25 min): Teach using examples from specific pages\n"
                "- Activity (10 min): Use practice problems from the material\n"
                "- Conclusion (5 min): Summarize and assign homework\n\n"
                "Reference the material's page numbers throughout.\n"
            )

        else:
            # Standard behavior without uploaded material
            if is_bed_qualified:
                context_parts.append(
                    f"You are helping a B.Ed/M.Ed qualified teacher understand '{topic_name}' for Grade {grade} {subject}.\n\n"
                    "Since they already have pedagogical training, focus ONLY on the subject content:\n"
                    "- Provide an in-depth, comprehensive explanation of the concept\n"
                    "- Include advanced examples and edge cases\n"
                    "- Highlight common student misconceptions\n"
                    "- Provide challenging practice problems\n"
                    "- Do NOT include basic teaching tips - they already know pedagogy\n\n"
                    f"Explain {topic_name} thoroughly and academically.\n"
                )
            else:
                # NON-B.ED TEACHER: Natural flow approach
                context_parts.append(
                    f"You are helping a teacher WITHOUT B.Ed qualification understand and teach '{topic_name}' to Grade {grade} {subject} students.\n\n"

                    "IMPORTANT: Provide a NATURAL, FLOWING response (not broken into parts).\n\n"

                    "YOUR RESPONSE STRUCTURE (seamlessly blended, not separated):\n"
                    "1. Start by explaining the CONCEPT in a clear, simple, beginner-friendly way (60% of response)\n"
                    "   - What is this concept? Use simple language\n"
                    "   - Why is it important for Grade {grade} students?\n"
                    "   - Key terms explained with analogies\n"
                    "   - Visual descriptions (how to draw/show it)\n"
                    "   - Real-world connections that make it relatable\n\n"

                    "2. Then naturally transition to EXAMPLES and practice (30% of response)\n"
                    "   - 3-4 solved examples with step-by-step explanations\n"
                    "   - 3 practice problems (beginner to intermediate)\n"
                    "   - Common mistakes students make\n"
                    "   - Real-world applications\n\n"

                    "3. Finally, end with brief TEACHING TIPS (10% of response, keep it short and practical)\n"
                    "   - How to introduce this topic (one quick suggestion)\n"
                    "   - One interactive activity idea\n"
                    "   - Common mistakes to watch for when teaching\n\n"
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

    async def _retrieve_from_material(
        self,
        material_id: int,
        topic: str,
        material_filename: Optional[str] = None
    ) -> tuple:
        """
        Retrieve relevant chunks from uploaded teaching material
        Returns: (material_chunks, material_source_info)
        """
        try:
            vector_store = get_vector_store()
            collection_name = f"material_{material_id}"

            # Check if collection exists
            if not vector_store.collection_exists(collection_name):
                print(f"[AI TUTOR] Collection {collection_name} does not exist")
                return [], None

            # Search for relevant chunks based on topic
            results = vector_store.search_similar_chunks(
                collection_name=collection_name,
                query=topic,
                n_results=10  # Get more chunks for comprehensive context
            )

            # Format chunks for context
            material_chunks = []
            if results and 'documents' in results and len(results['documents']) > 0:
                for idx, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][idx]
                    material_chunks.append({
                        'content': doc,
                        'page_number': metadata.get('page_number', 'N/A'),
                        'section_title': metadata.get('section_title', ''),
                        'relevance': 1 - results['distances'][0][idx]  # Convert distance to similarity
                    })

            # Prepare source info for response
            material_source = {
                'filename': material_filename,
                'chunks_retrieved': len(material_chunks),
                'pages': list(set([c['page_number'] for c in material_chunks if c['page_number'] != 'N/A']))
            }

            print(f"[AI TUTOR] Retrieved {len(material_chunks)} chunks from {material_filename}")
            return material_chunks, material_source

        except Exception as e:
            print(f"[AI TUTOR ERROR] Failed to retrieve from material: {e}")
            return [], None

    def clear_session(self, session_id: int):
        """Clear session from memory"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]

        # Also clear Garuda conversation ID
        if session_id in self.garuda_conversations:
            del self.garuda_conversations[session_id]

# Initialize orchestrator
ai_tutor_orchestrator = AITutorOrchestrator()
