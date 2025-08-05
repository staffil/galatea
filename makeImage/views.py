import os
import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def make_image_page(request):
    return render(request, "makeImage/image.html")

@csrf_exempt
@login_required
def generate_image(request):
    if request.method == "POST":
        user_input = request.POST.get("prompt")
        if not user_input:
            return JsonResponse({"error": "No prompt provided"}, status=400)

        response = client.images.generate(
            model="dall-e-3",
            prompt=user_input,
            n=1,
            size="1024x1024",
            quality="hd"
        )

        image_url = response.data[0].url
        return JsonResponse({"image_url": image_url})

    return JsonResponse({"error": "Invalid request"}, status=400)
@login_required
def proxy_image(request):
    image_url = request.GET.get("url")
    if not image_url:
        return HttpResponse("No URL provided", status=400)
    
    resp = requests.get(image_url)
    if resp.status_code != 200:
        return HttpResponse("Failed to fetch image", status=400)
    
    content_type = resp.headers.get('Content-Type', 'image/png')
    return HttpResponse(resp.content, content_type=content_type)
