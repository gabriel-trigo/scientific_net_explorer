import os
from django.shortcuts import render
from django.http import JsonResponse
from models.sample_models import MyType

def index(request):
    print(os.getenv('SEMANTIC_SCHOLAR_API_KEY'))
    print(os.getcwd())
    return JsonResponse({'key': 'nothing here'}, status=200)

# Create your views here.
