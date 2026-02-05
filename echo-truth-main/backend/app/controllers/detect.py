"""
detect.py
Detection controller - orchestrates the detection pipeline

This is the main controller that coordinates:
1. Audio fetching/decoding
2. Feature extraction
3. Classification decision
4. Response formatting
"""

import os
import uuid
from typing import Optional
from app.services.audio_service import AudioService
from app.services.decision_service import DecisionService
from app.config import settings


class DetectController:
    """
    Controller for voice detection pipeline
    
    Orchestrates the full detection flow:
    audio → features → decision → response
    """
    
    def __init__(self):
        self.audio_service = AudioService()
        self.decision_service = DecisionService()
        self.temp_dir = settings.TEMP_DIR
        
        # Ensure temp directory exists
        os.makedirs(self.temp_dir, exist_ok=True)
    
    async def detect(
        self,
        audio_url: Optional[str] = None,
        audio_base64: Optional[str] = None,
        language: str = "en",
    ) -> dict:
        """
        Main detection method
        
        Flow:
        1. Download/decode audio to temp file
        2. Convert to WAV mono 16kHz
        3. Extract audio features
        4. Run classification
        5. Clean up temp files
        6. Return result
        
        Args:
            audio_url: URL to download audio from
            audio_base64: Base64 encoded audio data
            language: Language code (en, hi, ta, te, ml)
            
        Returns:
            dict with classification, confidence, explanation
            
        Raises:
            ValueError: If audio processing fails
        """
        temp_files = []
        
        try:
            # Generate unique temp file names
            file_id = str(uuid.uuid4())[:8]
            input_path = os.path.join(self.temp_dir, f"{file_id}_input.mp3")
            wav_path = os.path.join(self.temp_dir, f"{file_id}_processed.wav")
            temp_files.extend([input_path, wav_path])
            
            # Step 1: Get audio file
            if audio_url:
                await self.audio_service.download_audio(audio_url, input_path)
            elif audio_base64:
                await self.audio_service.decode_base64(audio_base64, input_path)
            else:
                raise ValueError("No audio provided")
            
            # Step 2: Convert to WAV mono 16kHz
            await self.audio_service.convert_to_wav(input_path, wav_path)
            
            # Step 3: Extract features
            features = await self.audio_service.extract_features(wav_path)
            
            # Step 4: Run classification
            result = await self.decision_service.classify(
                features=features,
                language=language,
            )
            
            return result
            
        finally:
            # Step 5: Clean up temp files
            for temp_file in temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except Exception as e:
                    print(f"Warning: Failed to clean up {temp_file}: {e}")
