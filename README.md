# 🤖 ChatGPT Voice Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production--Ready-success)

**A production-grade, hands-free voice assistant powered by OpenAI GPT-4o**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Configuration](#-configuration)

</div>

---

## 📋 Overview

A **professional, modular voice assistant** that enables natural conversation with ChatGPT through voice. Built with enterprise-grade architecture, this system demonstrates advanced integration of speech recognition, natural language processing, and text-to-speech technologies.

### **Key Capabilities**

- 🎤 **Wake Word Detection**: Local, low-latency activation using Picovoice Porcupine
- 🗣️ **Speech Recognition**: Real-time transcription with faster-whisper (optimized Whisper)
- 🧠 **AI Processing**: Intelligent responses powered by OpenAI GPT-4o
- 🔊 **Natural Speech**: Text-to-speech with configurable voices and speech parameters
- 🏗️ **Modular Architecture**: Clean, maintainable code structure for production deployment

---

## ✨ Features

### **Technical Features**

- **Hands-Free Operation**: Complete voice-controlled interaction cycle
- **Low Latency**: Optimized pipeline for near real-time responses
- **Conversation Memory**: Maintains context across multiple exchanges
- **Automatic Silence Detection**: Smart recording with voice activity detection
- **Graceful Error Handling**: Robust error recovery and user feedback
- **Configurable Components**: Easily adjust models, parameters, and behavior
- **Production Logging**: Comprehensive logging system for debugging and monitoring
- **Cross-Platform**: Compatible with Windows, macOS, and Linux

### **User Experience**

- Natural wake word activation ("Hey ChatGPT")
- Automatic speech detection and silence-based recording stop
- Conversational AI responses optimized for voice interaction
- Audio feedback for system status
- Clean console output with conversation history

---

## 🚀 Installation

### **Prerequisites**

- Python 3.10 or higher
- Microphone and speakers/headphones
- Internet connection (for OpenAI API)
- API Keys:
  - [OpenAI API Key](https://platform.openai.com/api-keys)
  - [Picovoice Access Key](https://console.picovoice.ai/)

### **Step 1: Clone Repository**

```bash
git clone https://github.com/yourusername/chatgpt-voice-assistant.git
cd chatgpt-voice-assistant
```

### **Step 2: Create Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Note for Windows users**: If you encounter issues with `pyaudio`, install it via:
```bash
pip install pipwin
pipwin install pyaudio
```

### **Step 4: Download Wake Word Model**

1. Go to [Picovoice Console](https://console.picovoice.ai/)
2. Create a custom wake word "Hey ChatGPT"
3. Download the `.ppn` model file for your platform
4. Place it in the `models/` directory as `Hey-ChatGPT_en_windows_v3_0_0.ppn`

### **Step 5: Configure Environment**

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# Required:
#   OPENAI_API_KEY=sk-...
#   PICOVOICE_ACCESS_KEY=...
```

---

## 💻 Usage

### **Basic Usage**

```bash
python assistant.py
```

The assistant will:
1. Initialize all components
2. Display configuration summary
3. Wait for wake word "Hey ChatGPT"
4. Listen to your question
5. Process and respond via voice

### **Testing Individual Components**

**Test Wake Word Detection:**
```bash
python wakeword.py
```

**Test Speech-to-Text:**
```bash
python stt.py
```

**Test ChatGPT API:**
```bash
python chatgpt_api.py
```

**Test Text-to-Speech:**
```bash
python tts.py
```

---

## 🏗️ Architecture

### **System Design**

```
┌─────────────────────────────────────────────────────────┐
│                   Voice Assistant                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │  Wake Word   │───→│     STT      │                 │
│  │   Detection  │    │  (Whisper)   │                 │
│  └──────────────┘    └──────┬───────┘                 │
│                              │                          │
│                              ↓                          │
│                      ┌──────────────┐                  │
│                      │   ChatGPT    │                  │
│                      │   (GPT-4o)   │                  │
│                      └──────┬───────┘                  │
│                              │                          │
│                              ↓                          │
│                      ┌──────────────┐                  │
│                      │     TTS      │                  │
│                      │  (pyttsx3)   │                  │
│                      └──────────────┘                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### **Project Structure**

```
chatgpt-voice-assistant/
│
├── assistant.py          # Main application orchestrator
├── config.py            # Centralized configuration management
├── wakeword.py          # Wake word detection module
├── stt.py               # Speech-to-text engine
├── chatgpt_api.py       # OpenAI ChatGPT integration
├── tts.py               # Text-to-speech engine
│
├── models/              # Wake word model files (.ppn)
├── logs/                # Application logs
│
├── .env                 # Environment variables (not in repo)
├── .env.example         # Environment template
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

### **Module Descriptions**

| Module | Responsibility | Key Technologies |
|--------|---------------|------------------|
| `config.py` | Configuration management, API keys, parameters | python-dotenv |
| `wakeword.py` | Local wake word detection | Picovoice Porcupine |
| `stt.py` | Audio recording and transcription | faster-whisper, PyAudio |
| `chatgpt_api.py` | ChatGPT conversation management | OpenAI API |
| `tts.py` | Text-to-speech synthesis | pyttsx3 |
| `assistant.py` | System orchestration and main loop | Threading, asyncio |

---

## ⚙️ Configuration

### **Key Configuration Parameters**

Edit `config.py` to customize behavior:

```python
# Wake Word
WAKE_WORD_SENSITIVITY = 0.5        # Detection sensitivity (0.0-1.0)

# Speech-to-Text
STT_MODEL = "base"                  # Model size: tiny/base/small/medium/large
STT_LANGUAGE = "en"                 # Language code
RECORDING_TIMEOUT = 10              # Max recording duration (seconds)
SILENCE_DURATION = 1.5              # Silence to stop recording

# ChatGPT
CHATGPT_MODEL = "gpt-4o"           # OpenAI model
CHATGPT_MAX_TOKENS = 500           # Response length limit
CHATGPT_TEMPERATURE = 0.7          # Response creativity (0.0-2.0)

# Text-to-Speech
TTS_VOICE_RATE = 175               # Speech speed (WPM)
TTS_VOICE_INDEX = 1                # Voice selection (0=male, 1=female)

# System
LOG_LEVEL = "INFO"                 # Logging verbosity
MAX_CONVERSATION_HISTORY = 10      # Context window size
```

---

## 🔧 Advanced Features

### **Custom Wake Words**

1. Create custom wake word at [Picovoice Console](https://console.picovoice.ai/)
2. Download `.ppn` file
3. Update `WAKE_WORD_MODEL_PATH` in `config.py`

### **Model Selection**

**Whisper Model Tradeoff:**
- `tiny`: Fastest, less accurate (~1GB RAM)
- `base`: Good balance (~1GB RAM)
- `small`: Better accuracy (~2GB RAM)
- `medium`: High accuracy (~5GB RAM)
- `large-v3`: Best accuracy (~10GB RAM)

**ChatGPT Model Options:**
- `gpt-4o`: Latest, most capable (recommended)
- `gpt-4o-mini`: Faster, more economical
- `gpt-4-turbo`: Previous generation

### **Voice Customization**

List available voices:
```python
python tts.py
```

Change voice in `config.py`:
```python
TTS_VOICE_INDEX = 0  # Try different indices
```

---

## 🐛 Troubleshooting

### **Common Issues**

**PyAudio Installation Failed (Windows)**
```bash
pip install pipwin
pipwin install pyaudio
```

**Wake Word Not Detected**
- Check microphone permissions
- Increase `WAKE_WORD_SENSITIVITY` (0.0-1.0)
- Verify `.ppn` model file exists in `models/`
- Test wake word: `python wakeword.py`

**STT Not Working**
- Ensure microphone is default input device
- Test recording: `python stt.py`
- Try different `STT_MODEL` size

**OpenAI API Errors**
- Verify API key in `.env`
- Check account balance/quota
- Test API: `python chatgpt_api.py`

**No Audio Output**
- Check speaker/headphone connection
- Verify default audio output device
- Test TTS: `python tts.py`

---

## 📊 Performance Metrics

| Component | Latency | Resource Usage |
|-----------|---------|----------------|
| Wake Word Detection | <100ms | Minimal CPU |
| Speech Recording | 1-10s | Low CPU |
| STT Transcription | 1-3s | Medium CPU/GPU |
| ChatGPT API | 1-5s | Network only |
| TTS Synthesis | <1s | Low CPU |
| **Total Response Time** | **3-15s** | **Moderate** |

---

## 🛠️ Technology Stack

### **Core Technologies**

- **Python 3.10+**: Primary programming language
- **OpenAI GPT-4o**: Natural language understanding and generation
- **Picovoice Porcupine**: Wake word detection engine
- **faster-whisper**: Optimized speech recognition (CTranslate2-based)
- **pyttsx3**: Cross-platform text-to-speech
- **PyAudio**: Audio I/O library

### **Dependencies**

| Library | Purpose | Version |
|---------|---------|---------|
| `openai` | GPT-4o API client | ≥1.12.0 |
| `pvporcupine` | Wake word detection | ≥3.0.0 |
| `faster-whisper` | Speech recognition | ≥0.10.0 |
| `pyttsx3` | Text-to-speech | ≥2.90 |
| `pyaudio` | Audio I/O | ≥0.2.13 |
| `numpy` | Numerical operations | ≥1.24.0 |
| `python-dotenv` | Environment management | ≥1.0.0 |

---

## 🔐 Security & Privacy

- **API Keys**: Stored securely in `.env` (never committed to git)
- **Local Processing**: Wake word detection runs entirely offline
- **Data Transmission**: Only transcribed text sent to OpenAI API
- **No Recording Storage**: Audio not saved to disk by default
- **Conversation Privacy**: History stored in memory only (not persisted)

---

## 📈 Future Enhancements

### **Planned Features**

- [ ] **Orca Streaming TTS**: Lower latency speech synthesis
- [ ] **GPU Acceleration**: Faster STT with CUDA support
- [ ] **Multi-Language**: Support for languages beyond English
- [ ] **Custom Commands**: Pre-programmed actions (timers, weather, etc.)
- [ ] **Conversation Export**: Save/load conversation history
- [ ] **Web Dashboard**: Browser-based control interface
- [ ] **Docker Deployment**: Containerized deployment option
- [ ] **Cloud Integration**: AWS/Azure deployment guides

### **Potential Integrations**

- **Home Automation**: Control smart home devices
- **Calendar/Email**: Integration with productivity tools
- **Knowledge Base**: RAG system for company documentation
- **Multi-User**: User identification and personalization

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### **Code Standards**

- Follow PEP 8 style guide
- Add type hints to function signatures
- Include docstrings for all public methods
- Write unit tests for new features
- Update README for significant changes

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**[Your Name]**  
*AI Engineer | Full-Stack Developer*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/yourprofile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/yourusername)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-green)](https://yourwebsite.com)

---

## 🌟 Project Highlights

### **Portfolio Summary**

This project demonstrates:

- ✅ **Advanced AI Integration**: Production-grade implementation of multiple AI services
- ✅ **System Architecture**: Modular, scalable design patterns
- ✅ **API Proficiency**: OpenAI GPT-4o, Picovoice Porcupine integration
- ✅ **Audio Processing**: Real-time speech recognition and synthesis
- ✅ **Python Expertise**: Advanced Python patterns, async programming, threading
- ✅ **Production Quality**: Error handling, logging, configuration management
- ✅ **Documentation**: Comprehensive technical documentation
- ✅ **Best Practices**: Type hints, modular design, clean code principles

### **Technical Skills Demonstrated**

| Category | Skills |
|----------|--------|
| **AI/ML** | GPT-4o, Whisper, Speech Processing, NLP |
| **Python** | asyncio, threading, type hints, OOP |
| **APIs** | OpenAI, Picovoice, REST integration |
| **Audio** | PyAudio, signal processing, VAD |
| **DevOps** | Environment management, logging, testing |
| **Architecture** | Modular design, separation of concerns |

### **Business Impact**

- **Customer Service**: Hands-free AI assistant for support desks
- **Accessibility**: Voice-controlled interfaces for users with disabilities
- **Smart Home**: Integration hub for home automation
- **Enterprise**: Internal AI assistant for employee productivity
- **Healthcare**: HIPAA-compliant voice documentation system
- **Education**: Language learning and tutoring applications

---

## 📚 References

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Picovoice Porcupine Docs](https://picovoice.ai/docs/porcupine/)
- [faster-whisper GitHub](https://github.com/guillaumekln/faster-whisper)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/)

---

## 💬 Support

For issues, questions, or suggestions:

- 📧 Email: your.email@example.com
- 💼 LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/chatgpt-voice-assistant/issues)

---

<div align="center">

**⭐ Star this repository if you find it useful!**

Made with ❤️ by [Your Name]

</div>
