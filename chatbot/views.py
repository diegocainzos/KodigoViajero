from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
import json
from .services.orquestrator import procesar_mensaje_usuario
from .services.nlp_service import extract_tourism_info
from .models import Destinations


class HomePageView(TemplateView):
    template_name = "home.html"


class HtmxPageView(TemplateView):
    template_name = "htmlx.html"


class ChatPageView(TemplateView):
    template_name = "chatbot.html"


def chatbot_api(request):
    if request.method == "POST":
        # Supports HTMX form (request.POST) and JSON
        msg = request.POST.get("message")
        if msg is None:
            try:
                body = json.loads(request.body or "{}")
            except json.JSONDecodeError:
                body = {}
            msg = body.get("message", "")

        reply = procesar_mensaje_usuario(msg)
        print(reply, type(reply))

        # If it's an HTMX request, return an HTML fragment with the updated textarea
        if request.headers.get("HX-Request") == "true":
            user_message = request.POST.get("message", "")
            respuesta = procesar_mensaje_usuario(user_message)

            # Format with line breaks to append to the history
            formatted_message = f"\nYou: {user_message}\nBot: {respuesta}\n"

            return HttpResponse(formatted_message)

        # Regular JSON API
        return JsonResponse({"reply": str(reply)})
