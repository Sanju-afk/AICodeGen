import os
from dotenv import load_dotenv
import openai
import requests

#Load environment variables
load_dotenv()
API_TOKEN = os.getenv("API_KEY")  # .env key must be GROQ_API_KEY


# Configure Groq API
openai.api_key = API_TOKEN
openai.base_url = "https://api.groq.com/openai/v1/"  # Critical trailing slash

def generate_code(prompt: str, language: str) -> str:
    try:
        response = openai.chat.completions.create(
            model="llama3-70b-8192",  # Valid Groq model name
            messages=[
                {
                    "role": "user",
                    "content": f"Provide the complete code for {prompt} in {language} and give the code only"
                }
            ],
            max_tokens=300,
            temperature=0.7,
            stop=["\n\n\n\n"]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ Error: {e}")
        raise
