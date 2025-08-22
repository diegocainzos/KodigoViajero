import os
import requests
import spacy 
from django.http import JsonResponse
import json
from dotenv import load_dotenv
# Get token from environment variable for security


load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
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
    """
    Crea un prompt avanzado para que el LLM genere una respuesta final,
    conversacional y visualmente atractiva usando los datos de hoteles.
    """
    # Convertimos los datos a un string JSON bien formateado para el prompt.
    # Limitar la cantidad de hoteles aquí si es necesario para no exceder el contexto.
    hoteles_json_string = json.dumps(datos_hoteles[:3], indent=2, ensure_ascii=False)

    # El prompt mejorado con instrucciones claras y ejemplos (few-shot prompting)
    return f"""
# ROL Y OBJETIVO
Eres Kódigo, un asistente de viajes virtual, experto en encontrar las mejores opciones para los usuarios. Tu tono es amigable, servicial y un poco entusiasta. Tu misión es transformar datos brutos de hoteles en una respuesta clara, útil y visualmente atractiva.

# CONTEXTO
Un usuario te ha hecho la siguiente petición: "{mensaje_usuario}"
Tras buscar en tu sistema, has obtenido estos datos en formato JSON:
```json
{hoteles_json_string}
```

# TAREA Y REGLAS DE FORMATO
Ahora, crea una respuesta conversacional para el usuario. Debes seguir estas reglas OBLIGATORIAMENTE:

1.  **Inicio Conversacional:** Comienza con un saludo amigable. Resume en una frase lo que has encontrado. Ejemplo: "¡Genial! He encontrado algunas opciones fantásticas para ti en [Ciudad]. ¡Échales un vistazo!"

2.  **Estructura Visual y Markdown:**
    *   Usa un título claro para la lista, como `## 🏨 Hoteles Recomendados en [Ciudad]`.
    *   Presenta cada hotel como un ítem de una lista con viñetas (`*`).
    *   Utiliza emojis para hacer la información más digerible: 💰 para el precio, ⭐ para la puntuación, 📝 para la descripción, etc.

3.  **Enlaces Clicables (CRÍTICO):**
    *   El nombre de cada hotel DEBE ser un enlace clicable en formato Markdown, usando el campo `enlace_google`.
    *   El formato debe ser: `**[Nombre del Hotel](enlace_google)**`. Usa negrita para que destaque.

4.  **Resumen Conciso y Preciso:**
    *   Debajo del nombre del hotel, resume los detalles clave en una o dos líneas.
    *   Ejemplo: `💰 Precio: [precio] - ⭐ Puntuación: [puntuacion] ([total_opiniones] opiniones)`

5.  **Cero Invenciones (IMPORTANTE):**
    *   Solo puedes usar la información presente en el JSON proporcionado.
    *   Si un dato (como `puntuacion` o `precio`) no está disponible para un hotel, indica claramente "No disponible" o simplemente omite esa parte. NO INVENTES NINGÚN DATO.

6.  **Cierre Amigable:** Termina la respuesta con una pregunta abierta o una frase que invite a seguir la conversación. Ejemplo: "¿Qué te parecen estas opciones? ¿Quieres que busque más detalles sobre alguna?"

# EJEMPLO DE SALIDA PERFECTA:
¡Hola! Encontré algunas opciones excelentes para tu viaje a Madrid. ¡Aquí tienes un resumen!

## 🏨 Hoteles Recomendados en Madrid

*   **[Hotel Ritz Madrid](https://www.google.com/hotels/entity/...)**
    💰 Precio: 500€ - ⭐ Puntuación: 4.8 (1200 opiniones)
    📝 Un hotel de lujo histórico con vistas espectaculares al parque.

*   **[Hotel Urban](https://www.google.com/hotels/entity/...)**
    💰 Precio: 250€ - ⭐ Puntuación: 4.5 (850 opiniones)
    📝 Famoso por su diseño vanguardista y su piscina en la azotea.

¿Te gustaría que mirara la disponibilidad o buscara otro tipo de alojamiento? ¡Tú mandas!
"""
