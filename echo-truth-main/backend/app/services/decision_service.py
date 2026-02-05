"""
decision_service.py
Classification decision service

Makes the final AI vs Human classification decision.
Uses LLM for reasoning with heuristic fallback.

Flow:
1. Try LLM-based classification
2. If LLM fails → use heuristic fallback
3. Return standardized result
"""

from typing import Dict, Any
from app.services.ai_service import AIService


class DecisionService:
    """
    Service for making classification decisions
    
    Primary: LLM-based reasoning
    Fallback: Heuristic rules based on feature thresholds
    """
    
    def __init__(self):
        self.ai_service = AIService()
    
    async def classify(
        self,
        features: Dict[str, Any],
        language: str = "en",
    ) -> Dict[str, Any]:
        """
        Classify audio as AI-generated or human
        
        Args:
            features: Extracted audio features
            language: Audio language code
            
        Returns:
            Dict with:
            - classification: "AI_GENERATED" | "HUMAN"
            - confidence: float 0.0-1.0
            - explanation: str (max 240 chars)
        """
        try:
            # Try LLM-based classification
            result = await self.ai_service.classify_with_llm(features, language)
            
            if result and self._validate_result(result):
                return result
            
        except Exception as e:
            print(f"LLM classification failed, using fallback: {e}")
        
        # Fallback to heuristic classification
        return self._heuristic_classify(features)
    
    def _validate_result(self, result: Dict[str, Any]) -> bool:
        """
        Validate LLM result has required fields and valid values
        """
        if not isinstance(result, dict):
            return False
        
        classification = result.get("classification")
        confidence = result.get("confidence")
        explanation = result.get("explanation")
        
        if classification not in ["AI_GENERATED", "HUMAN"]:
            return False
        
        if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
            return False
        
        if not isinstance(explanation, str) or len(explanation) == 0:
            return False
        
        return True
    
    def _heuristic_classify(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback heuristic classification
        
        ============================================
        HEURISTIC RULES
        ============================================
        AI-generated audio typically has:
        - Low pitch variance (consistent, synthetic tone)
        - Low silence ratio (no natural pauses)
        - Consistent volume (processed/normalized)
        
        Human audio typically has:
        - Higher pitch variance (natural intonation)
        - More silence (pauses, breathing)
        - Variable volume (natural dynamics)
        ============================================
        
        These thresholds are tuned heuristics, not ML predictions.
        Confidence is set low (0.55) to indicate uncertainty.
        """
        pitch_variance = features.get("pitch_variance", 0.5)
        silence_ratio = features.get("silence_ratio", 0.1)
        avg_volume = features.get("avg_volume", 0.05)
        
        # Heuristic scoring
        ai_score = 0.0
        reasons = []
        
        # Low pitch variance suggests AI
        if pitch_variance < 0.15:
            ai_score += 0.4
            reasons.append("consistent pitch patterns")
        
        # Low silence ratio suggests AI
        if silence_ratio < 0.05:
            ai_score += 0.3
            reasons.append("minimal natural pauses")
        
        # Very consistent volume suggests AI
        if 0.03 < avg_volume < 0.08:
            ai_score += 0.2
            reasons.append("normalized volume levels")
        
        # Make decision
        if ai_score >= 0.5:
            classification = "AI_GENERATED"
            explanation = f"Audio shows {', '.join(reasons) or 'synthetic characteristics'}. Features suggest machine-generated speech patterns."
        else:
            classification = "HUMAN"
            explanation = "Audio exhibits natural variations in pitch and rhythm consistent with authentic human speech patterns."
        
        # Low confidence for heuristic fallback
        confidence = 0.55
        
        return {
            "classification": classification,
            "confidence": confidence,
            "explanation": explanation[:240],  # Ensure max 240 chars
        }
