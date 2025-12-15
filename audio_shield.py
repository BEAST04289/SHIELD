import os
import json
import time
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI

load_dotenv()

# --- Configuration ---
SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

# AI Brain Configuration (GitHub Models or Azure OpenAI)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AOAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AOAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")

def transcribe_audio(audio_file_path):
    """
    Transcribes audio using Azure Speech Services.
    """
    if not SPEECH_KEY or not SPEECH_REGION:
        return None

    try:
        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        speech_config.speech_recognition_language="en-US"
        
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        # Future-proofing: For long audio, use start_continuous_recognition. 
        # For short clips (Imagine Cup demo), recognize_once is simpler.
        result = speech_recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
            return None
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
            return None
            
    except Exception as e:
        print(f"Transcription Error: {e}")
        return None

def analyze_audio_transcript(transcript, language="en"):
    """
    Analyzes the audio transcript using GitHub Models/Azure OpenAI.
    """
    client = None
    model_name = "gpt-4o"

    if GITHUB_TOKEN:
        client = AzureOpenAI(
            azure_endpoint="https://models.inference.ai.azure.com",
            api_key=GITHUB_TOKEN,
            api_version="2024-05-01-preview"
        )
        model_name = "gpt-4o"
    elif AOAI_ENDPOINT and AOAI_KEY:
        client = AzureOpenAI(
            azure_endpoint=AOAI_ENDPOINT,
            api_key=AOAI_KEY,
            api_version="2024-02-15-preview"
        )
        model_name = AOAI_DEPLOYMENT
    else:
        return None

    lang_instruction = ""
    if language == "hi":
        lang_instruction = "IMPORTANT: Provide the 'summary', 'red_flags', and 'advice' fields in HINDI (Devanagari script). Keep 'verdict_label' in English."

    system_prompt = f"""
    You are SHIELD, an expert scam detection AI. Your job is to analyze transcripts of voice messages or phone calls and determine if it is a scam.
    
    Analyze the text for:
    1. Urgency (pressure to act now)
    2. Impersonation (claiming to be bank, police, family)
    3. Requests for money, gift cards, or passwords
    4. Threats of arrest or account closure
    5. Robot-like phrasing or unnatural language

    {lang_instruction}

    Return a JSON object with this EXACT structure:
    {{
        "verdict_label": "SAFE" or "CAUTION" or "HIGH RISK",
        "confidence_score": 0-100 (integer),
        "summary": "A short, clear explanation of why.",
        "red_flags": ["Flag 1", "Flag 2", "Flag 3"],
        "advice": ["Step 1", "Step 2", "Step 3"]
    }}
    """

    user_prompt = f"Analyze this voice transcript:\n\n{transcript}"

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"GPT Error: {e}")
        return None
