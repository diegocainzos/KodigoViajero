from chatbot.services.chatbot_api_service import crear_prompt_decision, crear_prompt_sintesis, text_inference
from chatbot.services.serpi_service import hotel_query
import json


def procesar_mensaje_usuario(mensaje_usuario):
    """
    Main function that orchestrates the entire flow.
    """
    print(f"\n[Orchestrator] Processing message: '{mensaje_usuario}'")

    # 1. Decide whether a tool is needed
    prompt_decision = crear_prompt_decision(mensaje_usuario)
    respuesta_decision_str = text_inference(prompt=prompt_decision)

    print(f"[Orchestrator] LLM decision response: {respuesta_decision_str}")

    try:
        respuesta_decision = json.loads(respuesta_decision_str)
        print(respuesta_decision)
    except json.JSONDecodeError:
        print(
            "[Orchestrator] Error: The LLM did not return valid JSON. Answering directly.")
        respuesta_decision = {"decision": "answer_directly"}

    # 2. Act based on the decision
    if respuesta_decision.get("decision") == "use_tool":
        nombre_herramienta = respuesta_decision.get("name")
        parametros = respuesta_decision.get("parameters")

        if nombre_herramienta == "query_hotels" and parametros:
            print(
                f"[Orchestrator] LLM decided to use the 'query_hotels' tool for the location: '{parametros}'")
            print(parametros)
            # 3. Execute the local function (the tool)
            datos_hoteles = hotel_query(parametros)

            if not datos_hoteles:
                return "Sorry, I couldn't find hotels for that location. Would you like to try another place?"

            # 4. Synthesize the final answer with the data
            print(
                "[Orchestrator] Hotel data obtained. Asking the LLM to synthesize the response.")
            prompt_sintesis = crear_prompt_sintesis(
                mensaje_usuario, datos_hoteles)
            respuesta_final = text_inference(prompt=prompt_sintesis).strip()
            return respuesta_final
        else:

            return f"It looks like I need more information to help you with that. Could you be more specific? Tool: {nombre_herramienta}"

    else:  # Responder directamente
        print("[Orchestrator] LLM decided to answer directly.")
        prompt_simple = f"You are a travel assistant. Answer the following question in a friendly way: {mensaje_usuario}"
        respuesta_final = text_inference(prompt=prompt_simple).strip()
        return respuesta_final


def run_chat_loop():
    print("Hi! I'm your travel chatbot. Type 'exit' to finish.")
    while True:
        mensaje = input("You: ")
        if mensaje.lower() == 'exit':
            print("Chatbot: See you later!")
            break
        respuesta_bot = procesar_mensaje_usuario(mensaje)
        print(f"Chatbot: {respuesta_bot}")


"""
# --- Bucle principal para chatear ---
if __name__ == "__main__":
    print("Hi! I'm your travel chatbot. Type 'exit' to finish.")
    while True:
        mensaje = input("You: ")
        if mensaje.lower() == 'exit':
            print("Chatbot: See you later!")
            break
        
        respuesta_bot = procesar_mensaje_usuario(mensaje)
        print(f"Chatbot: {respuesta_bot}")
"""
