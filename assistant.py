"""
ChatGPT Voice Assistant - Main Application
Orchestrates wake word detection, STT, ChatGPT, and TTS
"""

import logging
import sys
from pathlib import Path
from typing import Optional
import threading
import time

# Import modules
from config import Config
from wakeword import WakeWordDetector
from stt import SpeechToText
from chatgpt_api import ChatGPTClient
from tts import TextToSpeech


class VoiceAssistant:
    """
    Main voice assistant class that orchestrates all components.
    Provides a complete hands-free voice interaction experience.
    """
    
    def __init__(self):
        """Initialize all assistant components."""
        self.running = False
        
        # Initialize components
        self.wake_word: Optional[WakeWordDetector] = None
        self.stt: Optional[SpeechToText] = None
        self.chatgpt: Optional[ChatGPTClient] = None
        self.tts: Optional[TextToSpeech] = None
        
        self.logger = logging.getLogger(__name__)
    
    def initialize(self) -> bool:
        """
        Initialize all assistant components.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        self.logger.info("Initializing Voice Assistant...")
        
        try:
            # Initialize Wake Word Detector
            self.logger.info("Loading wake word detector...")
            self.wake_word = WakeWordDetector(
                access_key=Config.PICOVOICE_ACCESS_KEY,
                model_path=str(Config.WAKE_WORD_MODEL_PATH),
                sensitivity=Config.WAKE_WORD_SENSITIVITY
            )
            
            # Initialize Speech-to-Text
            self.logger.info("Loading speech-to-text engine...")
            self.stt = SpeechToText(
                model_size=Config.STT_MODEL,
                device=Config.STT_DEVICE,
                compute_type=Config.STT_COMPUTE_TYPE,
                language=Config.STT_LANGUAGE
            )
            
            # Initialize ChatGPT Client
            self.logger.info("Connecting to ChatGPT API...")
            self.chatgpt = ChatGPTClient(
                api_key=Config.OPENAI_API_KEY,
                model=Config.CHATGPT_MODEL,
                max_tokens=Config.CHATGPT_MAX_TOKENS,
                temperature=Config.CHATGPT_TEMPERATURE,
                system_prompt=Config.SYSTEM_PROMPT
            )
            
            # Initialize Text-to-Speech
            self.logger.info("Loading text-to-speech engine...")
            self.tts = TextToSpeech(
                engine=Config.TTS_ENGINE,
                voice_rate=Config.TTS_VOICE_RATE,
                voice_index=Config.TTS_VOICE_INDEX
            )
            
            self.logger.info("✅ All components initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Initialization failed: {e}")
            self.cleanup()
            return False
    
    def handle_conversation(self) -> None:
        """
        Handle one complete conversation cycle:
        1. Record user speech
        2. Transcribe to text
        3. Get ChatGPT response
        4. Speak response
        """
        try:
            # Step 1: Record and transcribe user input
            self.logger.info("\n" + "="*60)
            self.logger.info("🎤 Listening for your question...")
            self.logger.info("="*60)
            
            user_text = self.stt.record_and_transcribe()
            
            if not user_text:
                self.tts.speak("I didn't catch that. Please try again.")
                return
            
            print(f"\n👤 You: {user_text}")
            
            # Step 2: Get ChatGPT response
            self.logger.info("🤔 Thinking...")
            response = self.chatgpt.send_message(user_text)
            
            if not response:
                self.tts.speak("I'm having trouble processing your request. Please try again.")
                return
            
            print(f"🤖 Assistant: {response}\n")
            
            # Step 3: Speak response
            self.tts.speak(response, blocking=True)
            
        except Exception as e:
            self.logger.error(f"Error during conversation: {e}")
            self.tts.speak("I encountered an error. Please try again.")
    
    def run(self) -> None:
        """
        Run the voice assistant in continuous mode.
        Listens for wake word, then handles conversation.
        """
        if not self.wake_word or not self.stt or not self.chatgpt or not self.tts:
            self.logger.error("Components not initialized. Call initialize() first.")
            return
        
        self.running = True
        
        # Start wake word detection
        if not self.wake_word.start():
            self.logger.error("Failed to start wake word detection")
            return
        
        # Welcome message
        print("\n" + "="*60)
        print("🎉 ChatGPT Voice Assistant Ready!")
        print("="*60)
        print("Say 'Hey ChatGPT' to activate")
        print("Press Ctrl+C to exit")
        print("="*60 + "\n")
        
        self.tts.speak("Voice assistant ready. Say hey chat G P T to activate.", blocking=True)
        
        try:
            # Main loop
            while self.running:
                # Listen for wake word
                if self.wake_word.listen_once():
                    print("\n✨ Wake word detected! Listening...\n")
                    
                    # Provide audio feedback
                    if Config.ENABLE_AUDIO_FEEDBACK:
                        self.tts.speak("Yes?", blocking=True)
                    
                    # Handle conversation
                    self.handle_conversation()
                    
                    # Brief pause before listening again
                    time.sleep(0.5)
                    print("\n👂 Listening for wake word...\n")
                
        except KeyboardInterrupt:
            print("\n\nShutting down assistant...")
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Stop the assistant."""
        self.running = False
        self.logger.info("Stopping voice assistant...")
    
    def cleanup(self) -> None:
        """Clean up all resources."""
        self.logger.info("Cleaning up resources...")
        
        if self.wake_word:
            self.wake_word.cleanup()
        
        if self.stt:
            self.stt.cleanup()
        
        if self.tts:
            self.tts.cleanup()
        
        self.logger.info("✓ Cleanup complete")


def setup_logging() -> None:
    """Configure logging for the application."""
    # Create logs directory
    Config.LOGS_DIR.mkdir(exist_ok=True)
    
    # Configure logging
    log_handlers = [logging.StreamHandler(sys.stdout)]
    
    if Config.LOG_TO_FILE:
        log_file = Config.LOGS_DIR / f"assistant_{time.strftime('%Y%m%d_%H%M%S')}.log"
        log_handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=Config.LOG_FORMAT,
        handlers=log_handlers
    )


def main():
    """Main entry point for the voice assistant."""
    print("\n" + "="*60)
    print("🤖 ChatGPT Voice Assistant")
    print("="*60)
    print("Production-Ready Voice AI System")
    print("Powered by OpenAI GPT-4o, Whisper, and Picovoice")
    print("="*60 + "\n")
    
    # Setup logging
    setup_logging()
    
    # Display configuration
    Config.display_config()
    
    # Validate configuration
    if not Config.validate():
        print("\n❌ Configuration validation failed. Please check your .env file.")
        print("Required: OPENAI_API_KEY and PICOVOICE_ACCESS_KEY")
        return 1
    
    # Initialize and run assistant
    assistant = VoiceAssistant()
    
    try:
        if not assistant.initialize():
            print("\n❌ Failed to initialize assistant")
            return 1
        
        assistant.run()
        
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        return 1
    
    finally:
        assistant.cleanup()
    
    print("\n👋 Thank you for using ChatGPT Voice Assistant!\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())