# -*- coding: utf-8 -*-
from django.urls import path

from app.accounts.views import UserAccountView, UserRelateGPTCarView, VisitLogView, BatchModelLimit, \
    UserChatGPTAccountList
from app.accounts.views.login import AccountLogin, UserFreeLoginView, AccountRegister

urlpatterns = [
    path("", UserAccountView.as_view()),
    path("register", AccountRegister.as_view()),
    path("login-free", UserFreeLoginView.as_view()),
    path("chatgpt-list", UserChatGPTAccountList.as_view()),
    path("batch-model-limit", BatchModelLimit.as_view()),
    path("relat-gptcar", UserRelateGPTCarView.as_view()),
    path("login", AccountLogin.as_view()),
    path("visit-log", VisitLogView.as_view()),
]
