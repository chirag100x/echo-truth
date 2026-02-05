"""
prompts.py
LLM prompt templates

Contains the classification prompt used for LLM-based detection.
"""


def get_classification_prompt(features: dict, language: str = "en") -> str:
    """
    Build the classification prompt for LLM
    
    The prompt instructs the LLM to:
    1. Analyze the provided audio features
    2. Apply forensic analysis rules
    3. Return a structured JSON response
    
    Args:
        features: Dict with duration, silence_ratio, avg_volume, pitch_variance
        language: Audio language code
        
    Returns:
        Formatted prompt string
    """
    
    # Format features for prompt
    features_str = f"""
- Duration: {features.get('duration', 0)} seconds
- Silence Ratio: {features.get('silence_ratio', 0):.2%}
- Average Volume (RMS): {features.get('avg_volume', 0):.6f}
- Pitch Variance (normalized): {features.get('pitch_variance', 0):.4f}
- Language: {language}
"""
    
    prompt = f"""You are an audio forensic analyst specializing in detecting AI-generated speech.

Given the following voice audio features:
{features_str}

ANALYSIS RULES:
- Overly consistent pitch (low pitch_variance < 0.15) → Suggests AI generation
- Lack of micro-pauses (low silence_ratio < 0.05) → Suggests AI generation  
- Very normalized volume levels → Suggests AI processing
- Natural pitch variation → Suggests human speech
- Presence of breathing pauses → Suggests human speech
- Variable volume dynamics → Suggests human speech

Based on these features and rules, determine if this audio is AI-generated or authentic human speech.

Return ONLY a valid JSON object with this exact structure:
{{
    "classification": "AI_GENERATED" or "HUMAN",
    "confidence": <number between 0 and 1>,
    "explanation": "<explanation in max 240 characters>"
}}

Important:
- Return ONLY the JSON, no other text
- Confidence should reflect certainty (0.5 = uncertain, 1.0 = very certain)
- Explanation should be concise and technical"""

    return prompt


def get_language_name(code: str) -> str:
    """Get full language name from code"""
    languages = {
        "en": "English",
        "hi": "Hindi",
        "ta": "Tamil",
        "te": "Telugu",
        "ml": "Malayalam",
    }
    return languages.get(code, "Unknown")
