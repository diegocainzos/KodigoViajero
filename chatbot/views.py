from django.http import JsonResponse
from django.views.generic import TemplateView
import json
from .services.chatbot_api_service import text_inference
from .services.nlp_service import extract_tourism_info
from .models import Destinations
class ChatPageView(TemplateView):
    template_name = "home.html"


def get_fake_flight(destination):
    return {"from": "BCN", "to": destination, "price": "120 EUR"}

def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        msg = data.get("message", "")
        if "Prague" in msg:
            destination = "Prague"
            days = 3
            return JsonResponse({"reply" : get_fake_flight(destination).get("to")}) 
        
        reply = text_inference(msg)
    

        data = reply.json()
        choice_0 = data["choices"][0]["message"]["content"]

        return JsonResponse({"reply": f"Bot dice: {choice_0}"})
    