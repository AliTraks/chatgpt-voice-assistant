# 🚀 Quick Start Guide

Get your ChatGPT Voice Assistant running in under 10 minutes!

---

## ✅ Pre-Installation Checklist

Before starting, ensure you have:

- [ ] **Python 3.10+** installed ([Download](https://www.python.org/downloads/))
- [ ] **Working microphone** and speakers/headphones
- [ ] **Internet connection** (for API calls)
- [ ] **OpenAI API Key** ([Get Here](https://platform.openai.com/api-keys))
- [ ] **Picovoice Access Key** ([Get Here](https://console.picovoice.ai/))

---

## 📦 Installation Steps

### 1️⃣ Clone & Navigate

```bash
git clone https://github.com/AliTraks/chatgpt-voice-assistant.git
cd chatgpt-voice-assistant
```

### 2️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**⚠️ Windows PyAudio Issue?** Install via:
```bash
pip install pipwin
pipwin install pyaudio
```

### 4️⃣ Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env file and add:
# OPENAI_API_KEY=sk-...
# PICOVOICE_ACCESS_KEY=...
```

### 5️⃣ Download Wake Word Model

1. Go to [Picovoice Console](https://console.picovoice.ai/)
2. Click "Create Wake Word"
3. Enter: **Hey ChatGPT**
4. Select your platform (Windows/Mac/Linux)
5. Download the `.ppn` file
6. Place in `models/` folder as `Hey-ChatGPT_en_windows_v3_0_0.ppn`

### 6️⃣ Verify Setup

```bash
python setup.py
```

This script checks:
- ✅ Python version
- ✅ Directory structure
- ✅ Environment variables
- ✅ Dependencies
- ✅ Wake word model

### 7️⃣ Run Assistant!

```bash
python assistant.py
```

**Expected Output:**
```
==============================
🤖 ChatGPT Voice Assistant
==============================
Production-Ready Voice AI System
Powered by OpenAI GPT-4o, Whisper, and Picovoice
==============================

Loading components...
✓ Wake word detection started
✓ Whisper model loaded
✓ ChatGPT API connected
✓ TTS engine ready

🎉 ChatGPT Voice Assistant Ready!
Say 'Hey ChatGPT' to activate
Press Ctrl+C to exit
```

---

## 🧪 Testing Components

Test each component individually:

### Test Wake Word Detection
```bash
python wakeword.py
```
Say "Hey ChatGPT" to test detection.

### Test Speech-to-Text
```bash
python stt.py
```
Speak after the prompt to test recording and transcription.

### Test ChatGPT API
```bash
python chatgpt_api.py
```
Sends test messages to verify API connection.

### Test Text-to-Speech
```bash
python tts.py
```
Plays test audio to verify speakers.

---

## 🎯 First Conversation

1. **Start the assistant:**
   ```bash
   python assistant.py
   ```

2. **Wait for ready message:**
   ```
   Voice assistant ready. Say hey chat G P T to activate.
   ```

3. **Activate with wake word:**
   Say: **"Hey ChatGPT"**

4. **Ask your question:**
   - "What's the weather like today?"
   - "Tell me a joke"
   - "Explain quantum computing simply"

5. **Wait for response:**
   The assistant will transcribe, process, and speak the answer.

---

## ⚙️ Quick Configuration

Edit `config.py` to customize:

```python
# Adjust wake word sensitivity (0.0 = less, 1.0 = more)
WAKE_WORD_SENSITIVITY = 0.5

# Change Whisper model (tiny/base/small/medium/large)
STT_MODEL = "base"

# Adjust speech speed (words per minute)
TTS_VOICE_RATE = 175

# Change logging level (DEBUG/INFO/WARNING/ERROR)
LOG_LEVEL = "INFO"
```

---

## 🐛 Common Issues & Fixes

### ❌ "Module not found" Error
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies:
pip install -r requirements.txt
```

### ❌ Wake Word Not Detecting
**Fix 1:** Increase sensitivity in `config.py`:
```python
WAKE_WORD_SENSITIVITY = 0.7
```

**Fix 2:** Check microphone permissions:
- Windows: Settings → Privacy → Microphone
- macOS: System Preferences → Security & Privacy → Microphone

### ❌ No Audio Output
**Check:**
1. Speakers/headphones connected
2. Volume not muted
3. Correct default audio device selected

**Test TTS:**
```bash
python tts.py
```

### ❌ "Invalid API Key"
**Fix:**
1. Verify API key in `.env` file
2. Check for extra spaces/quotes
3. Ensure key starts with `sk-`
4. Verify account has API access

### ❌ Slow Transcription
**Solutions:**
- Use smaller Whisper model: `STT_MODEL = "tiny"`
- Enable GPU: `STT_DEVICE = "cuda"` (requires CUDA setup)
- Close other applications

---

## 📊 Performance Expectations

| Component | Latency | Notes |
|-----------|---------|-------|
| Wake Word | <100ms | Local, instant |
| Recording | 1-10s | Depends on speech length |
| Transcription | 1-3s | Model dependent |
| ChatGPT API | 1-5s | Network dependent |
| TTS | <1s | Near instant |
| **Total** | **3-15s** | End-to-end |

---

## 🎓 Learning Path

**Beginner → Advanced:**

1. **Start:** Run with default settings
2. **Explore:** Test individual components
3. **Customize:** Adjust config parameters
4. **Extend:** Add custom commands
5. **Deploy:** Integrate with other systems

---

## 📚 Next Steps

✅ **Read Full Documentation:** [README.md](README.md)
✅ **Understand Architecture:** Review module docstrings
✅ **Customize Behavior:** Edit `config.py`
✅ **Add Features:** Extend modules
✅ **Deploy:** Containerize with Docker

---

## 🆘 Getting Help

**Resources:**
- 📖 Full README: [README.md](README.md)
- 🐛 GitHub Issues: [Report Bug](https://github.com/yourusername/chatgpt-voice-assistant/issues)
- 📧 Email: your.email@example.com
- 💼 LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

**Before Asking for Help:**
1. Run `python setup.py` to check configuration
2. Test components individually
3. Check logs in `logs/` directory
4. Review error messages carefully

---

## ✨ Tips for Best Experience

- 🎤 **Microphone:** Use quality microphone for better recognition
- 🔇 **Environment:** Minimize background noise
- 🗣️ **Speech:** Speak clearly at normal pace
- ⏱️ **Patience:** Wait for complete response before speaking again
- 🎛️ **Tuning:** Experiment with sensitivity and model settings

---

## 🎉 Congratulations!

You now have a working ChatGPT voice assistant!

**What's Next?**
- Share your experience on social media
- Star the repository ⭐
- Customize for your use case
- Build something amazing!

---

<div align="center">

**Questions? Issues? Feedback?**  
[Open an Issue](https://github.com/yourusername/chatgpt-voice-assistant/issues) | [LinkedIn](https://linkedin.com/in/yourprofile)

Made with ❤️ for the AI community

</div>
