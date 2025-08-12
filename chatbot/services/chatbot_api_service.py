import os
import requests
import spacy 
from django.http import JsonResponse

# Get token from environment variable for security
HF_TOKEN = os.environ.get('HF_TOKEN')
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is required. Please set it before running the application.")

API_URL = "https://router.huggingface.co/v1/chat/completions"

def text_inference(prompt):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "model": "openai/gpt-oss-20b",
    }

    return requests.post(API_URL, headers=headers, json=payload)
# print(response.json()["choices"][0]["message"])
    