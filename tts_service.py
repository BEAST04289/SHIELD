import os
import time
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

# --- Configuration ---
SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

def text_to_speech(text, language='en', output_file="output_tts.mp3"):
    """
    Converts text to speech using Azure Speech Services.
    Returns the path to the audio file.
    """
    if not SPEECH_KEY or not SPEECH_REGION:
        print("Azure Speech Key or Region missing.")
        return None

    try:
        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        
        # Set Voice based on Language
        if language == 'hi':
            # Hindi Voice (Female - Swara is a popular choice)
            speech_config.speech_synthesis_voice_name = "hi-IN-SwaraNeural" 
        else:
            # English Voice (Female - Ava is standard and clear)
            speech_config.speech_synthesis_voice_name = "en-US-AvaNeural"

        # Output to file
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
        
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return output_file
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech Synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
            return None

    except Exception as e:
        print(f"TTS Error: {e}")
        return None
