import os

from dotenv import load_dotenv
from google import genai


# Load variables from .env
load_dotenv()


# Check whether the API key exists
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:

    raise ValueError(
        "GEMINI_API_KEY was not found."
    )


# Create Gemini client
client = genai.Client(
    api_key=api_key
)


# Send a simple test request
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Say hello in one short sentence."
)


# Display Gemini response
print("\nGemini Response:")
print(response.text)