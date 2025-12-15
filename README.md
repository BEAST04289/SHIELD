<div align="center">

# 🛡️ SHIELD
### AI-Powered Family Scam Defense


[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Azure AI](https://img.shields.io/badge/Azure%20AI-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

*Protecting the vulnerable from digital fraud with the power of Generative AI.*

</div>

---

## 📖 Overview

**SHIELD** is an intelligent guardian designed to protect less tech-savvy users—especially the elderly—from the rising tide of digital scams. By leveraging **Azure AI Services** and **GPT-4o**, SHIELD provides real-time analysis of suspicious content across multiple modalities: text, image, and audio.

In an era where AI is used to *create* scams (deepfakes, voice cloning), SHIELD uses AI to *detect* and *defeat* them.

## ✨ Key Features

### 🛡️ Core Protection
| Feature | Description | Tech Stack |
|---------|-------------|------------|
| **📷 Visual Shield** | Analyzes screenshots, letters, or popups for visual scam indicators (fake logos, urgency). | Azure Computer Vision (OCR) + GPT-4o |
| **🎤 Audio Shield** | Transcribes and analyzes voice recordings to detect scam scripts and high-pressure tactics. | Azure Speech Services + GPT-4o |
| **💬 Text Shield** | Instantly flags phishing attempts, malicious links, and social engineering in messages. | GPT-4o |

### 👨‍👩‍👧‍👦 Family & Community
- **Family Shield Circle:** Create a safety network. High-risk threats automatically trigger alerts to designated family members.
- **Community Stats:** Track money saved and safety streaks to gamify protection.
- **Scam of the Week:** Weekly educational content to keep users informed about the latest fraud trends.

### 🌍 Accessibility & Inclusion
- **Multilingual Support:** Full interface and analysis support for **English** and **Hindi**.
- **Text-to-Speech:** Listen to analysis results for better accessibility.
- **Simple UI:** Designed with high contrast and large text for ease of use.

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **LLM Orchestration:** GitHub Models / Azure OpenAI
- **Computer Vision:** Azure AI Vision
- **Speech Processing:** Azure AI Speech
- **Language:** Python

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Azure Subscription (for Vision & Speech resources)
- GitHub Account (for GitHub Models access)

### Installation

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
   Create a `.env` file in the root directory with your API keys:
   ```env
   # Azure Computer Vision
   AZURE_CV_ENDPOINT="your_vision_endpoint"
   AZURE_CV_KEY="your_vision_key"

   # GitHub Models (GPT-4o)
   GITHUB_TOKEN="your_github_pat"

   # Azure Speech Services
   AZURE_SPEECH_KEY="your_speech_key"
   AZURE_SPEECH_REGION="your_speech_region"
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## 🔒 Privacy & Ethics

SHIELD is built with **Privacy by Design** principles:
- **No Data Retention:** Images and audio are processed in memory and discarded immediately after analysis.
- **User Control:** Users explicitly choose what to upload.
- **Transparency:** AI confidence scores are always displayed alongside results.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
Made with ❤️ for grandparents everywhere.
</div>
