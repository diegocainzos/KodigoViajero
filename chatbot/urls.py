from django.urls import path
from .views import ChatPageView, chatbot_api
from .services import text_inference
urlpatterns = [
    path("chat/", ChatPageView.as_view(), name="chat"),
    path("api/chatbot/", chatbot_api, name="chatbot_api"),
]
