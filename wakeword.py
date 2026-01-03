"""
Wake Word Detection Module
Uses Picovoice Porcupine for local, low-latency wake word detection
"""

import logging
import struct
from typing import Optional, Callable
import pvporcupine
import pyaudio
from config import Config

logger = logging.getLogger(__name__)


class WakeWordDetector:
    """
    Handles wake word detection using Picovoice Porcupine.
    Runs in a separate thread and triggers callback when wake word is detected.
    """
    
    def __init__(self, access_key: str, model_path: str, sensitivity: float = 0.5):
        """
        Initialize wake word detector.
        
        Args:
            access_key: Picovoice Access Key
            model_path: Path to .ppn wake word model file
            sensitivity: Detection sensitivity (0.0 to 1.0)
        """
        self.access_key = access_key
        self.model_path = model_path
        self.sensitivity = sensitivity
        
        self.porcupine: Optional[pvporcupine.Porcupine] = None
        self.audio_stream: Optional[pyaudio.Stream] = None
        self.pyaudio_instance: Optional[pyaudio.PyAudio] = None
        self.is_listening = False
        
        logger.info("WakeWordDetector initialized")
    
    def start(self) -> bool:
        """
        Initialize Porcupine and start listening for wake word.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        try:
            # Initialize Porcupine with custom wake word
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keyword_paths=[str(self.model_path)],
                sensitivities=[self.sensitivity]
            )
            
            # Initialize PyAudio
            self.pyaudio_instance = pyaudio.PyAudio()
            
            # Open audio stream
            self.audio_stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.porcupine.sample_rate,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            self.is_listening = True
            logger.info(f"✓ Wake word detection started (sensitivity: {self.sensitivity})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start wake word detection: {e}")
            self.cleanup()
            return False
    
    def listen_once(self) -> bool:
        """
        Listen for one detection cycle.
        
        Returns:
            bool: True if wake word detected, False otherwise
        """
        if not self.is_listening or not self.audio_stream or not self.porcupine:
            return False
        
        try:
            # Read audio frame
            pcm = self.audio_stream.read(
                self.porcupine.frame_length,
                exception_on_overflow=False
            )
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            
            # Process frame for wake word
            keyword_index = self.porcupine.process(pcm)
            
            if keyword_index >= 0:
                logger.info("🎤 Wake word detected!")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error during wake word detection: {e}")
            return False
    
    def listen_continuous(self, callback: Callable[[], None]) -> None:
        """
        Continuously listen for wake word and trigger callback when detected.
        This is a blocking operation - run in a separate thread.
        
        Args:
            callback: Function to call when wake word is detected
        """
        logger.info("👂 Listening for wake word...")
        
        while self.is_listening:
            if self.listen_once():
                callback()
    
    def stop(self) -> None:
        """Stop listening for wake word."""
        self.is_listening = False
        logger.info("Wake word detection stopped")
    
    def cleanup(self) -> None:
        """Release all resources."""
        self.stop()
        
        if self.audio_stream:
            try:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            except Exception as e:
                logger.error(f"Error closing audio stream: {e}")
            finally:
                self.audio_stream = None
        
        if self.porcupine:
            try:
                self.porcupine.delete()
            except Exception as e:
                logger.error(f"Error deleting Porcupine instance: {e}")
            finally:
                self.porcupine = None
        
        if self.pyaudio_instance:
            try:
                self.pyaudio_instance.terminate()
            except Exception as e:
                logger.error(f"Error terminating PyAudio: {e}")
            finally:
                self.pyaudio_instance = None
        
        logger.info("Wake word detector cleaned up")
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()


def test_wake_word():
    """Test wake word detection standalone."""
    import time
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format=Config.LOG_FORMAT
    )
    
    print("\n" + "="*60)
    print("🎤 Wake Word Detection Test")
    print("="*60)
    print(f"Wake Word: Hey ChatGPT")
    print(f"Model: {Config.WAKE_WORD_MODEL_PATH}")
    print("Say the wake word to test detection...")
    print("Press Ctrl+C to exit")
    print("="*60 + "\n")
    
    def on_wake_word():
        print("✓ Wake word detected! [Test successful]")
    
    detector = WakeWordDetector(
        access_key=Config.PICOVOICE_ACCESS_KEY,
        model_path=str(Config.WAKE_WORD_MODEL_PATH),
        sensitivity=Config.WAKE_WORD_SENSITIVITY
    )
    
    try:
        if detector.start():
            detector.listen_continuous(on_wake_word)
    except KeyboardInterrupt:
        print("\n\nTest stopped by user")
    finally:
        detector.cleanup()


if __name__ == "__main__":
    test_wake_word()