import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print("Key loaded:", api_key[:10])

client = genai.Client(api_key=api_key)

# Small delay to avoid rate limit
time.sleep(2)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello and introduce yourself in one line!"
)
print(response.text)