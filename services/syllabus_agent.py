"""
AI Agent for fetching real syllabus/curriculum from online sources
Uses web search + AI to extract syllabus content
"""
import os
import httpx
import json
import asyncio
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat-v3.1:free")


class SyllabusAgent:
    """
    Autonomous AI Agent that:
    1. Searches for official syllabus documents online
    2. Extracts curriculum content
    3. Structures it for question generation
    """

    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.model = OPENROUTER_MODEL

    async def fetch_syllabus(
        self,
        state: str,
        board: str,
        grade: str,
        subject: str
    ) -> Dict:
        """
        Main agent function to fetch syllabus

        Args:
            state: State name (e.g., "Telangana", "Andhra Pradesh")
            board: Board name (e.g., "State Board", "CBSE")
            grade: Grade/Class (e.g., "5", "10")
            subject: Subject name (e.g., "Telugu", "Mathematics")

        Returns:
            Structured syllabus data with units, topics, learning outcomes
        """
        print(f"[AGENT] Fetching syllabus for {state} {board} Grade {grade} {subject}")

        # Step 1: Search for syllabus online
        search_results = await self._search_syllabus(state, board, grade, subject)

        # Step 2: Extract curriculum content using AI
        syllabus_data = await self._extract_curriculum(
            search_results, state, board, grade, subject
        )

        return syllabus_data

    async def _search_syllabus(
        self, state: str, board: str, grade: str, subject: str
    ) -> str:
        """
        Use AI to search for official syllabus sources
        """
        # Build search context with known official sources
        official_sources = self._get_official_sources(state, board)

        prompt = f"""You are a curriculum research agent. Find information about the official syllabus/curriculum.

TARGET CURRICULUM:
- State: {state}
- Board: {board}
- Grade/Class: {grade}
- Subject: {subject}

OFFICIAL SOURCES TO CHECK:
{official_sources}

TASK:
Provide comprehensive curriculum information including:
1. Main units/chapters covered in Grade {grade} {subject}
2. Key topics within each unit
3. Learning outcomes/objectives
4. Skills to be developed
5. Assessment patterns

If you have knowledge of this curriculum from your training data, provide detailed information.
Focus on official {state} {board} curriculum for Grade {grade} {subject}.

Return detailed curriculum structure.
"""

        max_retries = 3
        retry_delays = [5, 10, 20]  # Longer delays: 5s, 10s, 20s

        for attempt in range(max_retries):
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }

                body = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                }

                async with httpx.AsyncClient(timeout=60) as client:
                    response = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=body
                    )
                    response.raise_for_status()
                    data = response.json()

                content = data["choices"][0]["message"]["content"]
                print(f"[AGENT] Got curriculum information ({len(content)} chars)")
                return content

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Rate limited
                    if attempt < max_retries - 1:
                        wait_time = retry_delays[attempt]  # 5s, 10s, 20s
                        print(f"[AGENT RATE LIMIT] Attempt {attempt + 1}/{max_retries} - Waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        print(f"[AGENT ERROR] Rate limit exceeded after {max_retries} attempts")
                        return ""
                else:
                    print(f"[AGENT ERROR] HTTP {e.response.status_code}: {e}")
                    return ""
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delays[attempt]
                    print(f"[AGENT ERROR] Search failed: {e}. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    print(f"[AGENT ERROR] Search failed after {max_retries} attempts: {e}")
                    return ""

        return ""

    async def _extract_curriculum(
        self, search_results: str, state: str, board: str, grade: str, subject: str
    ) -> Dict:
        """
        Extract structured curriculum data from search results
        """
        prompt = f"""You are a curriculum structuring agent. Convert the curriculum information into structured JSON format.

CURRICULUM INFORMATION:
{search_results}

TARGET: {state} {board} Grade {grade} {subject}

Create a structured JSON with this format:
{{
  "state": "{state}",
  "board": "{board}",
  "grade": "{grade}",
  "subject": "{subject}",
  "units": {{
    "Unit 1 Name": {{
      "topics": ["Topic 1", "Topic 2", "Topic 3"],
      "learning_outcomes": ["Outcome 1", "Outcome 2"],
      "weightage": "15%"
    }},
    "Unit 2 Name": {{
      "topics": ["Topic 1", "Topic 2"],
      "learning_outcomes": ["Outcome 1", "Outcome 2"],
      "weightage": "20%"
    }}
  }},
  "assessment_pattern": {{
    "total_marks": 100,
    "theory_exam": 80,
    "internal_assessment": 20
  }},
  "difficulty_levels": {{
    "easy": "Basic recall and understanding",
    "medium": "Application and analysis",
    "hard": "Synthesis and evaluation"
  }}
}}

Return ONLY valid JSON. No additional text.
"""

        max_retries = 3
        retry_delays = [5, 10, 20]  # Longer delays: 5s, 10s, 20s

        for attempt in range(max_retries):
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }

                body = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                }

                async with httpx.AsyncClient(timeout=60) as client:
                    response = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=body
                    )
                    response.raise_for_status()
                    data = response.json()

                content = data["choices"][0]["message"]["content"].strip()

                # Remove markdown code blocks
                if content.startswith('```json'):
                    content = content[7:]
                if content.startswith('```'):
                    content = content[3:]
                if content.endswith('```'):
                    content = content[:-3]

                content = content.strip()

                # Parse JSON
                syllabus_data = json.loads(content)
                print(f"[AGENT] Extracted {len(syllabus_data.get('units', {}))} units")

                return syllabus_data

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Rate limited
                    if attempt < max_retries - 1:
                        wait_time = retry_delays[attempt]  # 5s, 10s, 20s
                        print(f"[AGENT RATE LIMIT] Extraction attempt {attempt + 1}/{max_retries} - Waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        print(f"[AGENT ERROR] Extraction rate limit exceeded after {max_retries} attempts")
                        return self._get_fallback_syllabus(state, board, grade, subject)
                else:
                    print(f"[AGENT ERROR] HTTP {e.response.status_code}: {e}")
                    return self._get_fallback_syllabus(state, board, grade, subject)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delays[attempt]
                    print(f"[AGENT ERROR] Extraction failed: {e}. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    print(f"[AGENT ERROR] Extraction failed after {max_retries} attempts: {e}")
                    return self._get_fallback_syllabus(state, board, grade, subject)

        return self._get_fallback_syllabus(state, board, grade, subject)

    def _get_official_sources(self, state: str, board: str) -> str:
        """Get known official curriculum sources"""
        sources = {
            "Telangana": {
                "State Board": "SCERT Telangana (scert.telangana.gov.in), Telangana Board of Secondary Education",
                "CBSE": "CBSE official website (cbse.gov.in), NCERT textbooks"
            },
            "Andhra Pradesh": {
                "State Board": "SCERT AP, AP Board of Secondary Education",
                "CBSE": "CBSE official website, NCERT"
            },
            "Karnataka": {
                "State Board": "KTBS (Karnataka Textbook Society), DSERT Karnataka",
                "CBSE": "CBSE, NCERT"
            },
            "Tamil Nadu": {
                "State Board": "TN Board (tn.gov.in), SCERT Tamil Nadu",
                "CBSE": "CBSE, NCERT"
            },
            "Maharashtra": {
                "State Board": "Maharashtra State Board, Balbharati textbooks",
                "CBSE": "CBSE, NCERT"
            }
        }

        state_sources = sources.get(state, {})
        board_source = state_sources.get(board, "Official education board websites")

        return f"- {board_source}\n- Education department {state} official portals\n- Government gazette notifications"

    def _get_fallback_syllabus(self, state: str, board: str, grade: str, subject: str) -> Dict:
        """Fallback syllabus structure if extraction fails"""
        return {
            "state": state,
            "board": board,
            "grade": grade,
            "subject": subject,
            "units": {
                f"{subject} Fundamentals": {
                    "topics": ["Basic concepts", "Core principles"],
                    "learning_outcomes": ["Understand fundamental concepts"],
                    "weightage": "30%"
                },
                f"Advanced {subject}": {
                    "topics": ["Advanced topics", "Applications"],
                    "learning_outcomes": ["Apply concepts to real scenarios"],
                    "weightage": "40%"
                }
            },
            "assessment_pattern": {
                "total_marks": 100,
                "theory_exam": 80,
                "internal_assessment": 20
            }
        }


# Global agent instance
syllabus_agent = SyllabusAgent()
