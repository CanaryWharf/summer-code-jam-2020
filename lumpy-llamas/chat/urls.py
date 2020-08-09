from django.urls import path

from . import views


urlpatterns = [
    path('', views.chat_lobby, name='chat_lobby'),
    path('gotoroom/', views.go_to_chat_room, name='go_to_chat_room'),
    path('users/', views.chat_users, name='chat_users'),
    path('room/<str:room_name>/', views.chat_room, name='chat_room'),
]
