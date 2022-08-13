import json
import os

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

def home(request):
    print("This is a test ")
    html = "<html><body>Index</body></html>"
    return HttpResponse(html)

def send_json(request): 
    try : 
        cwd = os.getcwd()
        print(f"cwd : {cwd}")
        f = open(f"{cwd}/schema.json")
        
        data = json.load(f)
        f.close()
        return JsonResponse(data)

    except Exception as e: 
        print(e)
        print("Failed while sending zipcho Schema Json File")
