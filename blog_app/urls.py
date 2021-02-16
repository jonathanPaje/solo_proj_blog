from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register_page),
    path('login', views.login_page)
]