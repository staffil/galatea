from django.shortcuts import render, redirect
import os
from dotenv import load_dotenv
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
SUPERTONE_API_KEY = os.getenv("SUPERTONE_API_KEY")
# Create your views here.
print("supertone",SUPERTONE_API_KEY)

def call_supertone_tts(text, voice_id="sona_ko_001", style="neutral"):
    url = f"https://supertoneapi.com/v1/text-to-speech/{voice_id}"

    headers = {
        "x-sup-api-key": SUPERTONE_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "language": "ko",
        "style": style,
        "model": "sona_speech_1",
        "voice_settings": {
            "pitch_shift": 0,
            "pitch_variance": 1,
            "speed": 1
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f"Supertone API Error {response.status_code}: {response.text}")

    if response.status_code == 200:
        return response.content  # mp3 binary
    else:
        raise Exception(f"Supertone API Error: {response.status_code} - {response.text}")


import traceback

@csrf_exempt
def supertone_experiment(request):
    if request.method == "POST":
        text = request.POST.get("text")
        try:
            audio_data = call_supertone_tts(text)
            return HttpResponse(audio_data, content_type="audio/mpeg")
        except Exception as e:
            tb = traceback.format_exc()
            print(f"Exception: {e}\nTraceback:\n{tb}")
            return HttpResponse(str(e), status=500)
    return render(request, 'supertone/supertoneExperiment.html')
