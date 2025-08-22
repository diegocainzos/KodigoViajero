from chatbot.services.chatbot_api_service import crear_prompt_decision, crear_prompt_sintesis, text_inference
from chatbot.services.serpi_service import hotel_query
import json

def procesar_mensaje_usuario(mensaje_usuario):
    """
    Función principal que orquesta todo el flujo.
    """
    print(f"\n[Orquestador] Procesando mensaje: '{mensaje_usuario}'")

    # 1. Decidir si se necesita una herramienta
    prompt_decision = crear_prompt_decision(mensaje_usuario)
    respuesta_decision_str = text_inference(prompt=prompt_decision)
    
    print(f"[Orquestador] Respuesta de decisión del LLM: {respuesta_decision_str}")
    
    try:
        respuesta_decision = json.loads(respuesta_decision_str)
        print(respuesta_decision)
    except json.JSONDecodeError:
        print("[Orquestador] Error: El LLM no devolvió un JSON válido. Respondiendo directamente.")
        respuesta_decision = {"decision": "responder_directamente"}

    # 2. Actuar según la decisión
    if respuesta_decision.get("decision") == "usar_herramienta":
        nombre_herramienta = respuesta_decision.get("name")
        parametros = respuesta_decision.get("parameters")
        
        if nombre_herramienta == "query_hotels" and parametros:
            print(f"[Orquestador] LLM decidió usar la herramienta 'query_hotels' para la localización: '{parametros}'")
            print(parametros)
            # 3. Ejecutar la función local (la herramienta)
            datos_hoteles = hotel_query(parametros)

            if not datos_hoteles:
                return "Lo siento, no pude encontrar hoteles para esa localización. ¿Quieres intentar con otro lugar?"

            # 4. Sintetizar la respuesta final con los datos
            print("[Orquestador] Datos de hoteles obtenidos. Pidiendo al LLM que sintetice la respuesta.")
            prompt_sintesis = crear_prompt_sintesis(mensaje_usuario, datos_hoteles)
            respuesta_final = text_inference(prompt=prompt_sintesis).strip()
            return respuesta_final
        else:
            
            return f"Parece que necesito más información para ayudarte con eso. ¿Podrías especificar mejor?, {nombre_herramienta}"

    else: # Responder directamente
        print("[Orquestador] LLM decidió responder directamente.")
        prompt_simple = f"Eres un asistente de viajes. Responde de forma amigable a la siguiente pregunta: {mensaje_usuario}"
        respuesta_final = text_inference(prompt=prompt_simple).strip()
        return respuesta_final
    
def run_chat_loop():
    print("¡Hola! Soy tu chatbot de viajes. Escribe 'salir' para terminar.")
    while True:
        mensaje = input("Tú: ")
        if mensaje.lower() == 'salir':
            print("Chatbot: ¡Hasta luego!")
            break
        respuesta_bot = procesar_mensaje_usuario(mensaje)
        print(f"Chatbot: {respuesta_bot}")
"""
# --- Bucle principal para chatear ---
if __name__ == "__main__":
    print("¡Hola! Soy tu chatbot de viajes. Escribe 'salir' para terminar.")
    while True:
        mensaje = input("Tú: ")
        if mensaje.lower() == 'salir':
            print("Chatbot: ¡Hasta luego!")
            break
        
        respuesta_bot = procesar_mensaje_usuario(mensaje)
        print(f"Chatbot: {respuesta_bot}")
"""