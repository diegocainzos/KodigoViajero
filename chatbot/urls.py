from django.urls import path
from .views import ChatPageView, chatbot_api, HtmxPageView
from .services.nlp_service import extract_tourism_info
urlpatterns = [
    path("chat/", ChatPageView.as_view(), name="chat"),
    path("api/chatbot/", chatbot_api, name="chatbot_api"),
    path("api/text_test/", extract_tourism_info, name="text_processing"),
    path("htmx/", HtmxPageView.as_view(), name="htmx"),
]
