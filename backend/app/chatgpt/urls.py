# -*- coding: utf-8 -*-
from django.urls import path

from app.chatgpt.views.chatgpt import ChatGPTAccountView, ChatGPTLoginView, ChatGPTAccountEnum
from app.chatgpt.views.gptcar import GptCarView, GptCarEnum

urlpatterns = [
    path("enum", ChatGPTAccountEnum.as_view()),
    path("", ChatGPTAccountView.as_view()),
    path("login", ChatGPTLoginView.as_view()),
    path("car", GptCarView.as_view()),
    path("car-enum", GptCarEnum.as_view()),

]