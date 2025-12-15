import os
import time
import json
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from openai import AzureOpenAI

load_dotenv()

# --- Configuration ---
CV_ENDPOINT = os.getenv("AZURE_CV_ENDPOINT")
CV_KEY = os.getenv("AZURE_CV_KEY")

# AI Brain Configuration (GitHub Models or Azure OpenAI)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AOAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AOAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")

def get_ocr_text(image_stream):
    """
    Extracts text from an image stream using Azure Computer Vision.
    """
    if not CV_ENDPOINT or not CV_KEY:
        return None # Fallback to mock if no keys

    try:
        client = ComputerVisionClient(CV_ENDPOINT, CognitiveServicesCredentials(CV_KEY))
        
        # Call the API
        read_response = client.read_in_stream(image_stream, raw=True)
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]

        # Wait for result
        while True:
            read_result = client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(0.5)

        # Extract text
        text_lines = []
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    text_lines.append(line.text)
        
        return "\n".join(text_lines)
    except Exception as e:
        print(f"OCR Error: {e}")
        return None

def analyze_with_gpt(ocr_text):
    """
    Analyzes the text using Azure OpenAI or GitHub Models to detect scams.
    """
    client = None
    model_name = "gpt-4o"

    if GITHUB_TOKEN:
        # Use GitHub Models (Free Tier)
        client = AzureOpenAI(
            azure_endpoint="https://models.inference.ai.azure.com",
            api_key=GITHUB_TOKEN,
            api_version="2024-05-01-preview"
        )
        model_name = "gpt-4o"
    elif AOAI_ENDPOINT and AOAI_KEY:
        # Use Azure OpenAI (Standard)
        client = AzureOpenAI(
            azure_endpoint=AOAI_ENDPOINT,
            api_key=AOAI_KEY,
            api_version="2024-02-15-preview"
        )
        model_name = AOAI_DEPLOYMENT
    else:
        return None

    system_prompt = """
    You are SHIELD, an expert scam detection AI. Your job is to analyze text from images (screenshots, letters, messages) and determine if it is a scam.
    
    Analyze the text for:
    1. Urgency (pressure to act now)
    2. Suspicious links or contacts
    3. Generic greetings or unprofessional language
    4. Too good to be true offers
    5. Threats of account suspension or legal action

    Return a JSON object with this EXACT structure:
    {
        "verdict_label": "SAFE" or "CAUTION" or "HIGH RISK",
        "confidence_score": 0-100 (integer),
        "summary": "A short, clear explanation of why.",
        "red_flags": ["Flag 1", "Flag 2", "Flag 3"],
        "advice": ["Step 1", "Step 2", "Step 3"]
    }
    """

    user_prompt = f"Analyze this text found in an image:\n\n{ocr_text}"

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

def analyze_image(file):
    """
    Main entry point for Visual Shield.
    """
    # 1. Reset file pointer
    file.seek(0)
    
    # 2. Perform OCR
    ocr_text = get_ocr_text(file)
    
    # 3. If OCR failed or no keys, return Mock Data (for demo/dev)
    if not ocr_text:
        # If we have no keys, we simulate a result for the "Dugtrio logo.jpg" or generic
        # This ensures the UI can be built even without keys working yet.
        return {
            "verdict_label": "HIGH RISK",
            "confidence_score": 88,
            "summary": "This appears to be a simulated scam alert (Demo Mode). The system detected urgency and suspicious patterns.",
            "red_flags": [
                "Urgent action required",
                "Suspicious link detected",
                "Unverified sender"
            ],
            "advice": [
                "Do not click any links",
                "Contact the official company directly",
                "Delete this message"
            ]
        }

    # 4. Analyze with GPT
    analysis = analyze_with_gpt(ocr_text)
    
    if analysis:
        return analysis
    else:
        # Fallback if GPT fails
        return {
            "verdict_label": "ERROR",
            "confidence_score": 0,
            "summary": "Could not analyze the image. Please try again.",
            "red_flags": [],
            "advice": []
        }