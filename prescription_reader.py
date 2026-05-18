import os
import time
from dotenv import load_dotenv
from google import genai
from pathlib import Path

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def read_prescription_image(image_path):
    # Read the image file
    image_data = Path(image_path).read_bytes()
    
    prompt = """
    You are a medical AI assistant helping elderly patients.
    This is a doctor's handwritten prescription.
    
    Please extract and convert it into a clear structured routine:
    - Medicine name (full name)
    - Dosage
    - Timing (Morning/Afternoon/Night)
    - Duration (number of days/weeks)
    - Special instructions (before food, after food etc.)
    
    Format it as a clean, easy to read table.
    """
    
    time.sleep(2)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": __import__('base64').b64encode(image_data).decode()
                        }
                    }
                ]
            }
        ]
    )
    return response.text

# Test with your prescription image
print("=== AI READING PRESCRIPTION ===\n")
result = read_prescription_image("prescription.jpg")
print(result)