import os
import requests
import spacy 

HF_TOKEN = "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"
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

nlp = spacy.load('en_core_web_md')

def text_processing(promt):
    doc = nlp(promt)
    