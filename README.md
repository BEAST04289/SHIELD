# 🛡️ SHIELD - Family Scam Defense

**Imagine Cup 2026 Entry**

SHIELD is an AI-powered guardian designed to protect less tech-savvy users (like elderly family members) from digital scams. It provides on-demand analysis of suspicious images, audio, and text using advanced Azure AI and OpenAI technologies.

## 🌟 Features

### 📷 Visual Shield
- **Input:** Screenshots, photos of letters, or popup images.
- **Tech:** Azure Computer Vision (OCR) + GPT-4o.
- **Function:** Extracts text from images and analyzes it for visual scam indicators (fake logos, urgency, threats).

### 🎤 Audio Shield
- **Input:** Voice recordings (WAV/MP3) of phone calls or voicemails.
- **Tech:** Azure Speech Services (Speech-to-Text) + GPT-4o.
- **Function:** Transcribes audio and detects scam scripts, impersonation (e.g., "Grandson in jail" scam), and high-pressure tactics.

### 💬 Text Shield
- **Input:** Direct text from SMS, WhatsApp, or Emails.
- **Tech:** GPT-4o.
- **Function:** Instantly flags phishing attempts, malicious links, and social engineering.

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Python)
- **AI Brain:** GitHub Models (GPT-4o) / Azure OpenAI
- **Vision:** Azure Computer Vision
- **Speech:** Azure Speech Services
- **Language:** Python 3.10+

## 🚀 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/BEAST04289/ImagineCup.git
   cd ImagineCup
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   Create a `.env` file with your keys:
   ```env
   AZURE_CV_ENDPOINT="your_vision_endpoint"
   AZURE_CV_KEY="your_vision_key"
   GITHUB_TOKEN="your_github_pat"
   AZURE_SPEECH_KEY="your_speech_key"
   AZURE_SPEECH_REGION="your_speech_region"
   ```

4. **Run the App**
   ```bash
   streamlit run app.py
   ```

## 🔒 Privacy & Ethics
SHIELD is designed with **Privacy by Design**:
- No data retention: Images and audio are processed in memory and discarded immediately.
- On-demand only: No "always-on" listening or watching. User initiates every check.

---
*Built for Microsoft Imagine Cup.*
