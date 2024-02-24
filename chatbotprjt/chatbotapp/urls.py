from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('send_message/', views.send_message, name='send_message'),
    path('clear_messages/', views.clear_messages, name='clear_messages'),
    path('select_suggestion/', views.select_suggestion, name='select_suggestion'),

    # Add other URL patterns as needed
]
