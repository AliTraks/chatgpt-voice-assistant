"""
Speech-to-Text Module
Uses faster-whisper for efficient, accurate transcription
"""

import logging
import wave
import tempfile
from pathlib import Path
from typing import Optional
import pyaudio
import numpy as np
from faster_whisper import WhisperModel
from config import Config

logger = logging.getLogger(__name__)


class SpeechToText:
    """
    Handles audio recording and transcription using faster-whisper.
    Optimized for low-latency, real-time transcription.
    """
    
    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8",
        language: str = "en"
    ):
        """
        Initialize Speech-to-Text engine.
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large-v3)
            device: Computation device (cpu, cuda)
            compute_type: Computation precision (int8, float16, float32)
            language: Target language for transcription
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.language = language
        
        self.model: Optional[WhisperModel] = None
        self.pyaudio_instance: Optional[pyaudio.PyAudio] = None
        
        logger.info(f"SpeechToText initializing with model: {model_size}")
        self._load_model()
    
    def _load_model(self) -> None:
        """Load Whisper model with specified configuration."""
        try:
            logger.info("Loading Whisper model... (this may take a moment)")
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type
            )
            logger.info("✓ Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    def record_audio(
        self,
        sample_rate: int = Config.AUDIO_SAMPLE_RATE,
        chunk_size: int = Config.AUDIO_CHUNK_SIZE,
        silence_threshold: int = Config.SILENCE_THRESHOLD,
        silence_duration: float = Config.SILENCE_DURATION,
        max_duration: int = Config.RECORDING_TIMEOUT
    ) -> Optional[np.ndarray]:
        """
        Record audio from microphone with automatic silence detection.
        
        Args:
            sample_rate: Audio sample rate in Hz
            chunk_size: Number of frames per buffer
            silence_threshold: Amplitude threshold for silence
            silence_duration: Seconds of silence to stop recording
            max_duration: Maximum recording duration in seconds
        
        Returns:
            numpy.ndarray: Recorded audio data, or None if recording failed
        """
        logger.info("🎙️  Recording audio... (speak now)")
        
        try:
            # Initialize PyAudio
            self.pyaudio_instance = pyaudio.PyAudio()
            
            # Open microphone stream
            stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk_size
            )
            
            frames = []
            silent_chunks = 0
            max_silent_chunks = int(silence_duration * sample_rate / chunk_size)
            max_chunks = int(max_duration * sample_rate / chunk_size)
            
            has_speech = False
            
            for _ in range(max_chunks):
                try:
                    data = stream.read(chunk_size, exception_on_overflow=False)
                    frames.append(data)
                    
                    # Convert to numpy array for amplitude analysis
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    amplitude = np.abs(audio_data).mean()
                    
                    # Detect speech vs silence
                    if amplitude > silence_threshold:
                        has_speech = True
                        silent_chunks = 0
                    elif has_speech:
                        silent_chunks += 1
                    
                    # Stop if silence detected after speech
                    if has_speech and silent_chunks > max_silent_chunks:
                        logger.info("Silence detected, stopping recording")
                        break
                        
                except Exception as e:
                    logger.error(f"Error reading audio chunk: {e}")
                    break
            
            # Cleanup
            stream.stop_stream()
            stream.close()
            self.pyaudio_instance.terminate()
            
            if not has_speech:
                logger.warning("No speech detected in recording")
                return None
            
            # Convert to numpy array
            audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
            audio_float = audio_data.astype(np.float32) / 32768.0  # Normalize to [-1, 1]
            
            logger.info(f"✓ Recording complete ({len(audio_float)/sample_rate:.1f}s)")
            return audio_float
            
        except Exception as e:
            logger.error(f"Audio recording failed: {e}")
            return None
    
    def transcribe(self, audio_data: np.ndarray) -> Optional[str]:
        """
        Transcribe audio data to text using Whisper.
        
        Args:
            audio_data: Audio data as numpy array (normalized float32)
        
        Returns:
            str: Transcribed text, or None if transcription failed
        """
        if self.model is None:
            logger.error("Whisper model not loaded")
            return None
        
        try:
            logger.info("🔄 Transcribing audio...")
            
            # Transcribe with faster-whisper
            segments, info = self.model.transcribe(
                audio_data,
                language=self.language,
                beam_size=5,
                vad_filter=True,  # Voice Activity Detection filter
                vad_parameters=dict(
                    threshold=0.5,
                    min_speech_duration_ms=250,
                    min_silence_duration_ms=500
                )
            )
            
            # Combine all segments
            transcription = " ".join([segment.text for segment in segments]).strip()
            
            if transcription:
                logger.info(f"✓ Transcription: '{transcription}'")
                return transcription
            else:
                logger.warning("Empty transcription result")
                return None
                
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return None
    
    def record_and_transcribe(self) -> Optional[str]:
        """
        Convenience method: Record audio and transcribe in one call.
        
        Returns:
            str: Transcribed text, or None if failed
        """
        audio_data = self.record_audio()
        if audio_data is None:
            return None
        
        return self.transcribe(audio_data)
    
    def cleanup(self) -> None:
        """Release resources."""
        if self.pyaudio_instance:
            try:
                self.pyaudio_instance.terminate()
            except Exception as e:
                logger.error(f"Error terminating PyAudio: {e}")
            finally:
                self.pyaudio_instance = None
        
        logger.info("STT engine cleaned up")


def test_stt():
    """Test speech-to-text standalone."""
    logging.basicConfig(
        level=logging.INFO,
        format=Config.LOG_FORMAT
    )
    
    print("\n" + "="*60)
    print("🎙️  Speech-to-Text Test")
    print("="*60)
    print("Speak after the prompt...")
    print("="*60 + "\n")
    
    stt = SpeechToText(
        model_size=Config.STT_MODEL,
        device=Config.STT_DEVICE,
        compute_type=Config.STT_COMPUTE_TYPE,
        language=Config.STT_LANGUAGE
    )
    
    try:
        text = stt.record_and_transcribe()
        if text:
            print(f"\n✓ Transcription Result: '{text}'")
        else:
            print("\n✗ Transcription failed")
    finally:
        stt.cleanup()


if __name__ == "__main__":
    test_stt()