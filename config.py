"""
Configuration Management Module
Centralized configuration for the ChatGPT Voice Assistant
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Centralized configuration class for all assistant components.
    Uses environment variables for sensitive data (API keys).
    """
    
    # ==================== Project Paths ====================
    BASE_DIR = Path(__file__).parent
    MODELS_DIR = BASE_DIR / "models"
    LOGS_DIR = BASE_DIR / "logs"
    
    # ==================== API Keys ====================
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    PICOVOICE_ACCESS_KEY: str = os.getenv("PICOVOICE_ACCESS_KEY", "")
    
    # ==================== Wake Word Configuration ====================
    WAKE_WORD_MODEL_PATH: Path = MODELS_DIR / "Hey-ChatGPT_en_windows_v3_0_0.ppn"
    WAKE_WORD_SENSITIVITY: float = 0.5  # Range: 0.0 to 1.0 (higher = more sensitive)
    
    # ==================== Speech-to-Text Configuration ====================
    STT_MODEL: str = "base"  # Options: tiny, base, small, medium, large-v2, large-v3
    STT_LANGUAGE: str = "en"  # ISO 639-1 language code
    STT_DEVICE: str = "cpu"  # Options: cpu, cuda
    STT_COMPUTE_TYPE: str = "int8"  # Options: int8, float16, float32
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_CHUNK_SIZE: int = 1024
    RECORDING_TIMEOUT: int = 10  # Maximum recording duration in seconds
    SILENCE_THRESHOLD: int = 500  # Amplitude threshold for silence detection
    SILENCE_DURATION: float = 1.5  # Seconds of silence to stop recording
    
    # ==================== ChatGPT Configuration ====================
    CHATGPT_MODEL: str = "gpt-4o"  # Latest model
    CHATGPT_MAX_TOKENS: int = 500
    CHATGPT_TEMPERATURE: float = 0.7
    CHATGPT_TIMEOUT: int = 30  # API request timeout in seconds
    SYSTEM_PROMPT: str = (
        "You are a helpful voice assistant. Provide concise, natural responses "
        "suitable for spoken conversation. Keep answers under 3 sentences unless "
        "more detail is specifically requested."
    )
    
    # ==================== Text-to-Speech Configuration ====================
    TTS_ENGINE: str = "pyttsx3"  # Options: pyttsx3, edge-tts, orca
    TTS_VOICE_RATE: int = 175  # Words per minute (for pyttsx3)
    TTS_VOICE_INDEX: int = 1  # Voice index (0 = male, 1 = female typically)
    
    # ==================== Logging Configuration ====================
    LOG_LEVEL: str = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_TO_FILE: bool = True
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # ==================== System Configuration ====================
    ENABLE_AUDIO_FEEDBACK: bool = True  # Play beep sounds for feedback
    MAX_CONVERSATION_HISTORY: int = 10  # Number of messages to keep in context
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required configurations are properly set.
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY not set in environment variables")
        
        if not cls.PICOVOICE_ACCESS_KEY:
            errors.append("PICOVOICE_ACCESS_KEY not set in environment variables")
        
        if not cls.MODELS_DIR.exists():
            cls.MODELS_DIR.mkdir(parents=True, exist_ok=True)
        
        if not cls.LOGS_DIR.exists():
            cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        if errors:
            print("❌ Configuration Errors:")
            for error in errors:
                print(f"   - {error}")
            return False
        
        return True
    
    @classmethod
    def display_config(cls) -> None:
        """Display current configuration (hiding sensitive data)."""
        print("\n" + "="*60)
        print("🔧 ChatGPT Voice Assistant Configuration")
        print("="*60)
        print(f"OpenAI API Key: {'✓ Set' if cls.OPENAI_API_KEY else '✗ Missing'}")
        print(f"Picovoice Key: {'✓ Set' if cls.PICOVOICE_ACCESS_KEY else '✗ Missing'}")
        print(f"STT Model: {cls.STT_MODEL}")
        print(f"ChatGPT Model: {cls.CHATGPT_MODEL}")
        print(f"TTS Engine: {cls.TTS_ENGINE}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print("="*60 + "\n")


# Validate configuration on import
if __name__ == "__main__":
    Config.validate()
    Config.display_config()