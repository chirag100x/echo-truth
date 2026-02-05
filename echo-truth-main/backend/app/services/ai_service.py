"""
ai_service.py
AI/LLM service for classification reasoning

============================================
LLM INTEGRATION
============================================
This service interfaces with LLM providers for
intelligent classification reasoning.

Supported providers (via LLM_PROVIDER env var):
- openai: OpenAI GPT-4
- gemini: Google Gemini
- groq: Groq (Llama)

API keys are loaded from config.py
============================================
"""

from typing import Dict, Any, Optional
from app.adapters.llm_adapter import LLMAdapter
from app.utils.prompts import get_classification_prompt


class AIService:
    """
    Service for LLM-powered classification
    
    Uses the LLM to analyze audio features and provide
    intelligent reasoning for the classification decision.
    """
    
    def __init__(self):
        self.llm = LLMAdapter()
    
    async def classify_with_llm(
        self,
        features: Dict[str, Any],
        language: str = "en",
    ) -> Optional[Dict[str, Any]]:
        """
        Use LLM to classify audio features
        
        Args:
            features: Extracted audio features
            language: Audio language code
            
        Returns:
            Dict with classification, confidence, explanation
            or None if LLM call fails
        """
        # Build prompt with features
        prompt = get_classification_prompt(features, language)
        
        # Call LLM
        response = await self.llm.generate(prompt)
        
        if not response:
            return None
        
        # Parse response
        result = self._parse_llm_response(response)
        
        return result
    
    def _parse_llm_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Parse LLM response into structured result
        
        Expected format from LLM:
        {
            "classification": "AI_GENERATED" | "HUMAN",
            "confidence": 0.0-1.0,
            "explanation": "..."
        }
        """
        import json
        
        try:
            # Try to extract JSON from response
            # Handle cases where LLM adds extra text
            response = response.strip()
            
            # Find JSON object in response
            start = response.find("{")
            end = response.rfind("}") + 1
            
            if start == -1 or end == 0:
                print(f"No JSON found in LLM response: {response[:100]}")
                return None
            
            json_str = response[start:end]
            result = json.loads(json_str)
            
            # Validate required fields
            if "classification" not in result:
                return None
            if "confidence" not in result:
                result["confidence"] = 0.7
            if "explanation" not in result:
                result["explanation"] = "Classification based on audio feature analysis."
            
            # Normalize classification value
            classification = result["classification"].upper().replace(" ", "_")
            if classification not in ["AI_GENERATED", "HUMAN"]:
                if "AI" in classification or "SYNTHETIC" in classification:
                    classification = "AI_GENERATED"
                else:
                    classification = "HUMAN"
            result["classification"] = classification
            
            # Ensure confidence is float
            result["confidence"] = float(result["confidence"])
            result["confidence"] = max(0.0, min(1.0, result["confidence"]))
            
            # Truncate explanation
            result["explanation"] = str(result["explanation"])[:240]
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM JSON: {e}")
            return None
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return None
