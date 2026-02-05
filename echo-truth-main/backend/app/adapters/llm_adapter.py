"""
llm_adapter.py
LLM provider adapter

============================================
LLM API KEYS
============================================
This adapter handles communication with LLM providers.

Configure via environment variables:
  LLM_PROVIDER: "openai" | "gemini" | "groq"
  LLM_API_KEY: Your provider API key

Get your API keys from:
  - OpenAI: https://platform.openai.com/api-keys
  - Google AI: https://makersuite.google.com/app/apikey
  - Groq: https://console.groq.com/keys
============================================
"""

from typing import Optional
from app.config import settings


class LLMAdapter:
    """
    Unified adapter for multiple LLM providers
    
    Supports:
    - OpenAI (GPT-4, GPT-3.5)
    - Google Gemini
    - Groq (Llama)
    
    ============================================
    TO SWAP LLM PROVIDERS:
    1. Set LLM_PROVIDER in .env (openai/gemini/groq)
    2. Set LLM_API_KEY in .env
    3. Optionally set LLM_MODEL for specific model
    ============================================
    """
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL
    
    async def generate(self, prompt: str) -> Optional[str]:
        """
        Generate LLM response
        
        Args:
            prompt: The prompt to send to LLM
            
        Returns:
            Generated text or None if failed
        """
        if not self.api_key:
            print("Warning: LLM_API_KEY not configured, skipping LLM call")
            return None
        
        try:
            if self.provider == "openai":
                return await self._call_openai(prompt)
            elif self.provider == "gemini":
                return await self._call_gemini(prompt)
            elif self.provider == "groq":
                return await self._call_groq(prompt)
            else:
                print(f"Unknown LLM provider: {self.provider}")
                return None
                
        except Exception as e:
            print(f"LLM call failed: {e}")
            return None
    
    async def _call_openai(self, prompt: str) -> Optional[str]:
        """
        Call OpenAI API
        
        ============================================
        OPENAI API KEY
        Get from: https://platform.openai.com/api-keys
        ============================================
        """
        import openai
        
        client = openai.OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model=self.model or "gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300,
        )
        
        return response.choices[0].message.content
    
    async def _call_gemini(self, prompt: str) -> Optional[str]:
        """
        Call Google Gemini API
        
        ============================================
        GEMINI API KEY
        Get from: https://makersuite.google.com/app/apikey
        ============================================
        """
        import google.generativeai as genai
        
        genai.configure(api_key=self.api_key)
        
        model = genai.GenerativeModel(self.model or "gemini-1.5-flash")
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 300,
            }
        )
        
        return response.text
    
    async def _call_groq(self, prompt: str) -> Optional[str]:
        """
        Call Groq API (Llama models)
        
        ============================================
        GROQ API KEY
        Get from: https://console.groq.com/keys
        ============================================
        """
        import requests
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model or "llama-3.1-8b-instant",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 300,
            },
            timeout=30,
        )
        
        response.raise_for_status()
        data = response.json()
        
        return data["choices"][0]["message"]["content"]
