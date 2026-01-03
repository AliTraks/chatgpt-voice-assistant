"""
Text-to-Speech Module
Converts ChatGPT responses to natural speech
Supports multiple TTS engines with fallback mechanism
"""

import logging
from typing import Optional
import pyttsx3
from config import Config

logger = logging.getLogger(__name__)


class TextToSpeech:
    """
    Handles text-to-speech conversion with configurable engines.
    Primary: pyttsx3 (offline, cross-platform)
    Future: Orca TTS, Edge TTS, or other streaming engines
    """
    
    def __init__(self, engine: str = "pyttsx3", voice_rate: int = 175, voice_index: int = 1):
        """
        Initialize Text-to-Speech engine.
        
        Args:
            engine: TTS engine to use (pyttsx3, edge-tts, orca)
            voice_rate: Speech rate in words per minute
            voice_index: Voice selection index
        """
        self.engine_name = engine
        self.voice_rate = voice_rate
        self.voice_index = voice_index
        
        self.engine: Optional[pyttsx3.Engine] = None
        
        logger.info(f"Initializing TTS engine: {engine}")
        self._initialize_engine()
    
    def _initialize_engine(self) -> None:
        """Initialize the TTS engine based on configuration."""
        try:
            if self.engine_name == "pyttsx3":
                self._initialize_pyttsx3()
            else:
                logger.warning(f"Unknown TTS engine: {self.engine_name}, falling back to pyttsx3")
                self._initialize_pyttsx3()
                
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            raise
    
    def _initialize_pyttsx3(self) -> None:
        """Initialize pyttsx3 TTS engine."""
        self.engine = pyttsx3.init()
        
        # Set speech rate
        self.engine.setProperty('rate', self.voice_rate)
        
        # Set voice (try to get female voice by default)
        voices = self.engine.getProperty('voices')
        if voices and len(voices) > self.voice_index:
            self.engine.setProperty('voice', voices[self.voice_index].id)
            logger.info(f"✓ Voice set to: {voices[self.voice_index].name}")
        
        # Set volume (0.0 to 1.0)
        self.engine.setProperty('volume', 0.9)
        
        logger.info("✓ pyttsx3 engine initialized successfully")
    
    def speak(self, text: str, blocking: bool = True) -> bool:
        """
        Convert text to speech and play it.
        
        Args:
            text: Text to convert to speech
            blocking: If True, wait for speech to complete
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not text or not text.strip():
            logger.warning("Empty text provided to TTS")
            return False
        
        if not self.engine:
            logger.error("TTS engine not initialized")
            return False
        
        try:
            logger.info(f"🔊 Speaking: '{text[:100]}...'")
            
            self.engine.say(text)
            
            if blocking:
                self.engine.runAndWait()
            
            return True
            
        except Exception as e:
            logger.error(f"TTS speech failed: {e}")
            return False
    
    def stop(self) -> None:
        """Stop current speech output."""
        if self.engine:
            try:
                self.engine.stop()
            except Exception as e:
                logger.error(f"Error stopping TTS: {e}")
    
    def set_rate(self, rate: int) -> None:
        """
        Change speech rate.
        
        Args:
            rate: Words per minute (typically 100-300)
        """
        if self.engine:
            self.engine.setProperty('rate', rate)
            self.voice_rate = rate
            logger.info(f"Speech rate changed to {rate} WPM")
    
    def set_volume(self, volume: float) -> None:
        """
        Change speech volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if self.engine:
            volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
            self.engine.setProperty('volume', volume)
            logger.info(f"Volume changed to {volume}")
    
    def list_voices(self) -> None:
        """List all available voices."""
        if not self.engine:
            logger.warning("Engine not initialized")
            return
        
        voices = self.engine.getProperty('voices')
        print("\nAvailable Voices:")
        print("="*60)
        for idx, voice in enumerate(voices):
            print(f"{idx}: {voice.name}")
            print(f"   ID: {voice.id}")
            print(f"   Languages: {voice.languages}")
            print()
    
    def cleanup(self) -> None:
        """Release TTS resources."""
        if self.engine:
            try:
                self.engine.stop()
            except Exception as e:
                logger.error(f"Error during TTS cleanup: {e}")
            finally:
                self.engine = None
        
        logger.info("TTS engine cleaned up")


def test_tts():
    """Test text-to-speech standalone."""
    logging.basicConfig(
        level=logging.INFO,
        format=Config.LOG_FORMAT
    )
    
    print("\n" + "="*60)
    print("🔊 Text-to-Speech Test")
    print("="*60)
    
    tts = TextToSpeech(
        engine=Config.TTS_ENGINE,
        voice_rate=Config.TTS_VOICE_RATE,
        voice_index=Config.TTS_VOICE_INDEX
    )
    
    # List available voices
    tts.list_voices()
    
    # Test speech
    test_texts = [
        "Hello! I am your ChatGPT voice assistant.",
        "I can help you with various tasks and answer your questions.",
        "How can I assist you today?"
    ]
    
    for text in test_texts:
        print(f"\n🔊 Speaking: {text}")
        success = tts.speak(text, blocking=True)
        if not success:
            print("✗ Speech failed")
    
    tts.cleanup()


if __name__ == "__main__":
    test_tts()