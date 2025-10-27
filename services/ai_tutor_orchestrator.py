import requests
from datetime import datetime
from typing import Dict, List
from services.model_config import AI_TUTOR_MODEL, OPENROUTER_API_KEY, OPENROUTER_BASE_URL
from services.rag_retrieval_service_local import rag_retrieval_service_local as rag_retrieval_service

class AITutorOrchestrator:
    def __init__(self):
        # OpenRouter API configuration
        self.api_key = OPENROUTER_API_KEY
        self.base_url = OPENROUTER_BASE_URL
        self.model = AI_TUTOR_MODEL

        # Store active sessions in memory
        self.active_sessions = {}

    async def start_session(
        self,
        session_id: int,
        teacher_id: int,
        topic_name: str,
        subject: str,
        grade: str,
        state: str,
        board: str,
        is_bed_qualified: bool
    ) -> Dict:
        """Start a new AI Tutor session"""

        print(f"[AI TUTOR] Starting session {session_id} for teacher {teacher_id}")
        print(f"[AI TUTOR] Topic: {topic_name}, Subject: {subject}, Grade: {grade}")
        print(f"[AI TUTOR] B.Ed Qualified: {is_bed_qualified}")

        # Step 1: Fetch real syllabus (placeholder for now)
        syllabus_content = f"{subject} Grade {grade} - {topic_name} (from {state} {board})"
        syllabus_fetched = True

        # Step 2: Retrieve pedagogy content (only for non-B.Ed teachers)
        pedagogy_chunks = []
        if not is_bed_qualified:
            print(f"[AI TUTOR] Retrieving pedagogy for non-B.Ed teacher...")
            rag_result = rag_retrieval_service.retrieve_for_ai_tutor(
                teacher_question=f"How to teach {topic_name}",
                subject=subject,
                grade=grade,
                is_bed_qualified=is_bed_qualified,
                top_k=5
            )
            pedagogy_chunks = rag_result["results"]

        # Step 3: Build context
        context = self._build_context(
            topic_name=topic_name,
            subject=subject,
            grade=grade,
            syllabus_content=syllabus_content,
            pedagogy_chunks=pedagogy_chunks,
            is_bed_qualified=is_bed_qualified
        )

        # Step 4: Generate AI response
        print(f"[AI TUTOR] Generating response with {self.model}...")
        response = self._generate_response(context)

        # Step 5: Store session in memory
        self.active_sessions[session_id] = {
            "topic_name": topic_name,
            "subject": subject,
            "grade": grade,
            "is_bed_qualified": is_bed_qualified,
            "messages": [
                {"role": "assistant", "content": response}
            ]
        }

        return {
            "session_id": session_id,
            "initial_message": response,
            "syllabus_fetched": syllabus_fetched,
            "pedagogy_sources": [
                {
                    "module": chunk["module"],
                    "subject": chunk["subject"],
                    "file_name": chunk["file_name"],
                    "relevance": chunk["relevance"]
                }
                for chunk in pedagogy_chunks
            ],
            "model_used": self.model,
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

        # Retrieve additional pedagogy if needed
        rag_result = rag_retrieval_service.retrieve_for_ai_tutor(
            teacher_question=user_message,
            subject=subject,
            grade=grade,
            is_bed_qualified=is_bed_qualified,
            top_k=3
        )
        pedagogy_chunks = rag_result["results"]

        # Get conversation history
        session = self.active_sessions.get(session_id, {})
        conversation_history = session.get("messages", [])

        # Add user message
        conversation_history.append({"role": "user", "content": user_message})

        # Build context
        context_parts = [f"Previous conversation:\n"]
        for msg in conversation_history[-4:]:  # Last 4 messages for context
            context_parts.append(f"{msg['role']}: {msg['content'][:200]}...\n")

        # Add new pedagogy
        if pedagogy_chunks:
            context_parts.append("\nAdditional Teaching Guidance:\n")
            for chunk in pedagogy_chunks:
                context_parts.append(f"- {chunk['content'][:300]}...\n")

        context_parts.append(f"\nTeacher's new question: {user_message}\n")
        context_parts.append("Provide a helpful, contextual response.")

        context = "".join(context_parts)

        # Generate response
        response = self._generate_response(context)

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
            "model_used": self.model,
            "timestamp": datetime.now().isoformat()
        }

    def _build_context(
        self,
        topic_name: str,
        subject: str,
        grade: str,
        syllabus_content: str,
        pedagogy_chunks: List[Dict],
        is_bed_qualified: bool
    ) -> str:
        """Build context for Claude"""

        context_parts = [
            f"You are an AI Teaching Assistant helping a Grade {grade} {subject} teacher.\n",
            f"Topic: {topic_name}\n",
            f"Syllabus: {syllabus_content}\n\n"
        ]

        if is_bed_qualified:
            context_parts.append(
                "This teacher has B.Ed/M.Ed qualification. Provide an in-depth subject explanation ONLY.\n"
                "Do NOT include basic teaching tips - they already know pedagogy.\n\n"
            )
        else:
            context_parts.append(
                "This teacher does NOT have B.Ed/M.Ed. Provide:\n"
                "1. SUBJECT EXPLANATION: What is this topic?\n"
                "2. TEACHING GUIDANCE: HOW to teach it (use the pedagogy below)\n\n"
            )

            if pedagogy_chunks:
                context_parts.append("IGNOU B.Ed Pedagogy References:\n")
                for i, chunk in enumerate(pedagogy_chunks, 1):
                    context_parts.append(f"{i}. {chunk['content'][:500]}...\n\n")

        context_parts.append(
            f"Provide a comprehensive response about teaching {topic_name} to Grade {grade} students."
        )

        return "".join(context_parts)

    def _generate_response(self, context: str) -> str:
        """Generate response using OpenRouter API"""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": context}
                ],
                "max_tokens": 4000,
                "temperature": 0.7
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )

            response.raise_for_status()
            result = response.json()

            response_text = result["choices"][0]["message"]["content"]
            print(f"[AI TUTOR] Generated {len(response_text)} characters")

            return response_text

        except Exception as e:
            print(f"[AI TUTOR ERROR] {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[AI TUTOR ERROR] Response: {e.response.text}")
            return f"I apologize, but I encountered an error. Please try again."

    def clear_session(self, session_id: int):
        """Clear session from memory"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]

# Initialize orchestrator
ai_tutor_orchestrator = AITutorOrchestrator()
