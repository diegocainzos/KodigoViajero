import os
import requests
import spacy 
from django.http import JsonResponse
import json
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

    response =  requests.post(API_URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]
    
tools = [
    {
        "name": "query_hotels",
        "description": "Busca hoteles en una localización específica, ordenados del más barato al más caro. Si el usuario indica algo sobre un viaje, selecciona esta herramineta, deberas usarla casi sin excepcion",
        "parameters": [
            {
                "name": "q",
                "type": "string",
                "description": "La ciudad o lugar donde buscar hoteles. Por ejemplo: 'París', 'Playa del Carmen, México'."
            },
            {
                "name" : "engine",
                "type" : "string",
                "description" : "El valor de este parametro sera siempre: google_hotels"
            },
            {
                "name": "check_in_date",
                "type": "string",
                "description": "Fecha de check-in en formato AAAA-MM-DD. Ejemplo: '2025-09-15'. En caso de no especificar un periodo concreto, te la inventas. Siempre posterior al 2025-10-01 "
            },
            {
                "name": "check_out_date",
                "type": "string",
                "description": "Fecha de check-out en formato AAAA-MM-DD. Ejemplo: '2025-09-16'.En caso de no especificar un periodo concreto, te la inventas. Siempre posterior al check_in_date que tambien te has inventado"
            },
            {
                "name": "adults",
                "type": "string",
                "description": "Número de adultos. Ejemplo: '2'."
            },
            {
                "name": "sort_by",
                "type": "string",
                "description": "Criterio de ordenamiento. Ejemplo: '3' para ordenar por precio. Pon 3 siempre"
            },
            {
                "name": "currency",
                "type": "string",
                "description": "Currency. Default option is EUR, but USD or other can be used if indicated."                
            },
        ]
    }
]

def crear_prompt_decision(mensaje_usuario):
    """Crea el prompt para que el LLM decida si usar una herramienta."""
    return f"""
Tu tarea es analizar el mensaje del usuario y decidir si necesitas llamar a una herramienta para responder.
Responde únicamente con un objeto JSON.

Herramientas disponibles:
{json.dumps(tools, indent=2)}

Si una herramienta es necesaria, responde con:
{{
  "decision": "usar_herramienta",
  "name": "nombre_de_la_herramienta",
  "parameters": {{ "nombre_parametro": "valor_extraido" }}
}}

Si no se necesita ninguna herramienta, responde con:
{{
  "decision": "responder_directamente"
}}

Mensaje del usuario: "{mensaje_usuario}"
"""

def crear_prompt_sintesis(mensaje_usuario, datos_hoteles):
    """Crea el prompt para que el LLM genere una respuesta final usando los datos."""
    # Tomamos solo los 3 primeros para no exceder el límite de tokens del prompt
    hoteles_resumidos = datos_hoteles
    return f"""
Eres un asistente de viajes amigable y servicial.
El usuario te preguntó: "{mensaje_usuario}"

Tú buscaste información y encontraste los siguientes hoteles, ordenados por precio:
{json.dumps(hoteles_resumidos, indent=2, ensure_ascii=False)}

Basándote en esta información, crea una respuesta conversacional y útil.
Resume los resultados de forma clara. Menciona el nombre, el precio y la puntuación si está disponible.
No inventes información que no esté en los datos proporcionados.
"""
