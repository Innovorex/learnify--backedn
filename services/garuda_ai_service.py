"""
Garuda AI Service
=================
Handles communication with Garuda AI API for AI Tutor functionality.
Provides conversation continuity and error handling.
"""

import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class GarudaAIService:
    """Service for interacting with Garuda AI API"""

    def __init__(self, api_key: str, base_url: str, model: str, timeout: int = 30):
        """
        Initialize Garuda AI Service

        Args:
            api_key: Garuda AI API key
            base_url: Base URL for Garuda AI API
            model: Model name to use
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.timeout = timeout

        logger.info(f"[GARUDA AI] Initialized with model: {model}")

    def generate_response(
        self,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict:
        """
        Generate a response from Garuda AI

        Args:
            message: The user message/prompt
            conversation_id: Optional conversation ID for continuity

        Returns:
            Dict with keys:
                - response: The AI response text
                - conversation_id: Conversation ID for continuity
                - request_id: Unique request ID
                - usage: Token usage information

        Raises:
            Exception: If API call fails
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "message": message,
                "conversation_id": conversation_id
            }

            endpoint = f"{self.base_url}/public/chat"

            logger.info(f"[GARUDA AI] Sending request to {endpoint}")
            logger.debug(f"[GARUDA AI] Payload: {payload}")

            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )

            response.raise_for_status()
            result = response.json()

            logger.info(f"[GARUDA AI] Response received successfully")
            logger.debug(f"[GARUDA AI] Response: {result}")

            # Validate response structure
            if "response" not in result:
                raise ValueError("Invalid response structure from Garuda AI")

            return {
                "response": result.get("response", ""),
                "conversation_id": result.get("conversation_id"),
                "request_id": result.get("request_id"),
                "usage": result.get("usage", {}),
                "model": result.get("model", self.model)
            }

        except requests.exceptions.Timeout:
            logger.error(f"[GARUDA AI] Request timeout after {self.timeout}s")
            raise Exception(f"Garuda AI request timeout after {self.timeout}s")

        except requests.exceptions.HTTPError as e:
            logger.error(f"[GARUDA AI] HTTP error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Garuda AI HTTP error: {e.response.status_code}")

        except requests.exceptions.RequestException as e:
            logger.error(f"[GARUDA AI] Request failed: {str(e)}")
            raise Exception(f"Garuda AI request failed: {str(e)}")

        except Exception as e:
            logger.error(f"[GARUDA AI] Unexpected error: {str(e)}")
            raise

    def test_connection(self) -> bool:
        """
        Test if Garuda AI API is reachable and working

        Returns:
            True if connection successful, False otherwise
        """
        try:
            result = self.generate_response("Hello")
            return bool(result.get("response"))
        except Exception as e:
            logger.error(f"[GARUDA AI] Connection test failed: {str(e)}")
            return False
