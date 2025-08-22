from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
import json
from .services.orquestrator import procesar_mensaje_usuario
from .services.nlp_service import extract_tourism_info
from .models import Destinations


class HtmxPageView(TemplateView):
    template_name = "htmlx.html"


class ChatPageView(TemplateView):
    template_name = "chatbot.html"


def chatbot_api(request):
    if request.method == "POST":
        # Soporta HTMX form (request.POST) y JSON
        msg = request.POST.get("message")
        if msg is None:
            try:
                body = json.loads(request.body or "{}")
            except json.JSONDecodeError:
                body = {}
            msg = body.get("message", "")

        reply = procesar_mensaje_usuario(msg)
        print(reply, type(reply))

        # Si viene de HTMX devolvemos un fragmento HTML con el textarea actualizado
        if request.headers.get("HX-Request") == "true":
            user_message = request.POST.get("message", "")
            respuesta = procesar_mensaje_usuario(user_message)

            # Formatear con saltos de línea para añadir al historial
            formatted_message = f"\nTú: {user_message}\nBot: {respuesta}\n"

            return HttpResponse(formatted_message)

        # API normal JSON
        return JsonResponse({"reply": str(reply)})
