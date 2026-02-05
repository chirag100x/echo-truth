"""
audio_service.py
Audio processing service

Handles:
- Downloading audio from URLs
- Decoding base64 audio
- Converting audio to WAV (mono 16kHz)
- Extracting audio features using librosa

Dependencies:
- requests: HTTP downloads
- ffmpeg-python: Audio conversion
- librosa: Feature extraction
- numpy: Numerical operations
"""

import os
import base64
import requests
import ffmpeg
import librosa
import numpy as np
from typing import Dict, Any


class AudioService:
    """
    Service for audio processing and feature extraction
    
    All audio is converted to:
    - Format: WAV
    - Channels: Mono
    - Sample rate: 16000 Hz
    
    This ensures consistent feature extraction.
    """
    
    # Supported audio formats
    SUPPORTED_FORMATS = {".mp3", ".wav", ".ogg", ".m4a", ".webm", ".flac"}
    
    # Target sample rate for processing
    TARGET_SAMPLE_RATE = 16000
    
    async def download_audio(self, url: str, output_path: str) -> None:
        """
        Download audio file from URL
        
        Args:
            url: HTTP/HTTPS URL to audio file
            output_path: Local path to save file
            
        Raises:
            ValueError: If download fails or URL is invalid
        """
        try:
            # Set timeout and user agent for reliable downloads
            headers = {
                "User-Agent": "EchoTruth/1.0 (Audio Analyzer)"
            }
            response = requests.get(url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get("Content-Type", "")
            if not ("audio" in content_type or "octet-stream" in content_type):
                print(f"Warning: Unexpected content type: {content_type}")
            
            # Save to file
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
        except requests.RequestException as e:
            raise ValueError(f"Failed to download audio: {str(e)}")
    
    async def decode_base64(self, base64_data: str, output_path: str) -> None:
        """
        Decode base64 audio data and save to file
        
        Args:
            base64_data: Base64 encoded audio (without data URL prefix)
            output_path: Local path to save decoded file
            
        Raises:
            ValueError: If decoding fails
        """
        try:
            # Remove data URL prefix if present
            if "," in base64_data:
                base64_data = base64_data.split(",")[1]
            
            # Decode and save
            audio_bytes = base64.b64decode(base64_data)
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
                
        except Exception as e:
            raise ValueError(f"Failed to decode base64 audio: {str(e)}")
    
    async def convert_to_wav(self, input_path: str, output_path: str) -> None:
        """
        Convert audio to WAV mono 16kHz using ffmpeg
        
        Args:
            input_path: Path to input audio file
            output_path: Path for output WAV file
            
        Raises:
            ValueError: If conversion fails
        """
        try:
            # FFmpeg conversion pipeline
            (
                ffmpeg
                .input(input_path)
                .output(
                    output_path,
                    acodec="pcm_s16le",  # 16-bit PCM
                    ac=1,                 # Mono
                    ar=self.TARGET_SAMPLE_RATE,  # 16kHz
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            raise ValueError(f"Audio conversion failed: {error_msg}")
    
    async def extract_features(self, wav_path: str) -> Dict[str, Any]:
        """
        Extract audio features for classification
        
        Features extracted:
        - duration: Length in seconds
        - silence_ratio: Proportion of silence in audio
        - avg_volume: Average RMS volume
        - pitch_variance: Variance in fundamental frequency (F0)
        
        Args:
            wav_path: Path to WAV file (mono 16kHz)
            
        Returns:
            Dict with extracted features
            
        Raises:
            ValueError: If feature extraction fails
        """
        try:
            # Load audio
            y, sr = librosa.load(wav_path, sr=self.TARGET_SAMPLE_RATE)
            
            # Duration
            duration = librosa.get_duration(y=y, sr=sr)
            
            # RMS (volume/energy)
            rms = librosa.feature.rms(y=y)[0]
            avg_volume = float(np.mean(rms))
            
            # Silence detection
            # Frames below 10% of max RMS are considered silence
            silence_threshold = np.max(rms) * 0.1
            silence_frames = np.sum(rms < silence_threshold)
            silence_ratio = float(silence_frames / len(rms)) if len(rms) > 0 else 0.0
            
            # Pitch (F0) using pyin
            f0, voiced_flag, voiced_probs = librosa.pyin(
                y, 
                fmin=librosa.note_to_hz('C2'),  # ~65 Hz
                fmax=librosa.note_to_hz('C7'),  # ~2093 Hz
                sr=sr,
            )
            
            # Calculate pitch variance (only on voiced frames)
            voiced_f0 = f0[~np.isnan(f0)]
            if len(voiced_f0) > 1:
                pitch_variance = float(np.var(voiced_f0))
                # Normalize pitch variance to 0-1 range (heuristic)
                pitch_variance = min(pitch_variance / 10000, 1.0)
            else:
                pitch_variance = 0.0
            
            return {
                "duration": round(duration, 2),
                "silence_ratio": round(silence_ratio, 4),
                "avg_volume": round(avg_volume, 6),
                "pitch_variance": round(pitch_variance, 4),
            }
            
        except Exception as e:
            raise ValueError(f"Feature extraction failed: {str(e)}")
