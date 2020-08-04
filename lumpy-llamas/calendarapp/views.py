from django.shortcuts import render
from django.http import JsonResponse


def get_calendar(request):
    return JsonResponse({'test': 'test'})

# Create your views here.
