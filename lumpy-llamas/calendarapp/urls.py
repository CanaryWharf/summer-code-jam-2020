from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('current', views.get_calendar, name='get_calendar')
]