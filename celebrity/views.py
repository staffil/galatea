import os
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from openai import OpenAI
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import base64
from user_auth.models import Celebrity
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import uuid
from payment.models import Token, TokenHistory

from django.conf import settings
load_dotenv(os.path.join(settings.BASE_DIR, ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
eleven_client = ElevenLabs(api_key=ELEVEN_API_KEY)
@login_required
@csrf_exempt
def make_ai(request):
    if request.method == "POST":
        return redirect("celebrity:child_view")

    return render(request, "customer_ai/make_ai2.html")

def celebrity_view(request, celebrity_id):
    celebrity = get_object_or_404(Celebrity, id=celebrity_id)
    language = request.LANGUAGE_CODE  # 현재 선택된 언어 코드 예: 'en', 'ko'

    # 다국어 필드명 생성
    name_field = f'celebrity_name_{language}'
    desc_field = f'description_{language}'

    # 해당 언어 필드가 있으면 사용, 없으면 기본 필드 사용
    celebrity.display_name = getattr(celebrity, name_field, celebrity.celebrity_name)
    celebrity.display_description = getattr(celebrity, desc_field, celebrity.description)

    context = {
        'celebrity': celebrity,
    }
    return render(request, "celebrity/celebrity.html", context)



@login_required
@csrf_exempt
def celebrity_audio(request):
    if request.method == 'POST':
        file = request.FILES.get('audio')
        if not file:
            return JsonResponse({"error": "No audio file provided."}, status=400)
        
        path = default_storage.save('audio/' + file.name, file)
        full_path = default_storage.path(path)
        
        with open(full_path, 'rb') as audio_file:
            transcription = openai_client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1"
            )
        return JsonResponse({"text": transcription.text})
    else:
        return HttpResponseNotAllowed(['POST'])
    



from pydub import AudioSegment

def get_audio_duration_in_seconds(file_path):
    audio = AudioSegment.from_file(file_path)
    return int(audio.duration_seconds)



@login_required
@csrf_exempt
def celebrity_response(request, celebrity_id):
    if request.method == 'POST':
        user_input = request.POST.get('text')
        if not user_input:
            return JsonResponse({"error": "텍스트를 입력하세요"}, status=400)

        user = request.user

        try:
            celebrity = get_object_or_404(Celebrity, id=celebrity_id)
        except Exception: # More specific exception could be used, e.g., Celebrity.DoesNotExist
            return JsonResponse({"error": "Celebrity not found."}, status=404)


        language_instructions = {
             'en': "You must respond ONLY in English.",
            'ko': "앞으로 모든 대답을 반드시 한국어로 해주세요.",
            'hi': "आपको केवल हिंदी में जवाब देना चाहिए।",
            'pt': "Você deve responder APENAS em português.",
            'zh': "你必须只用中文回答。",
            'es': "Debe responder SÓLO en español.",
            'fr': "Vous devez répondre UNIQUEMENT en français.",
            'ja': "必ず日本語で答えてください。",
            'ar': "يجب أن ترد فقط باللغة العربية.",
            'ru': "Вы должны отвечать ТОЛЬКО на русском языке.",
            'id': "Anda harus menjawab HANYA dalam bahasa Indonesia.",
            'it': "Devi rispondere SOLO in italiano.",
            'nl': "Je moet ALLEEN in het Nederlands antwoorden.",
            'tr': "Sadece Türkçe cevap vermelisiniz.",
            'pl': "Musisz odpowiadać TYLKO po polsku.",
            'sv': "Du måste svara ENDAST på svenska.",
            'fil': "Dapat kang sumagot LANG sa Filipino.",
            'ms': "Anda mesti menjawab HANYA dalam bahasa Melayu.",
            'ro': "Trebuie să răspunzi DOAR în limba română.",
            'uk': "Ви повинні відповідати ТІЛЬКИ українською мовою.",
            'el': "Πρέπει να απαντάτε ΜΟΝΟ στα ελληνικά.",
            'cs': "Musíte odpovídat POUZE v češtině.",
            'da': "Du skal kun svare på dansk.",
            'fi': "Sinun täytyy vastata VAIN suomeksi.",
            'bg': "Трябва да отговаряте САМО на български.",
            'hr': "Morate odgovarati SAMO na hrvatskom.",
            'sk': "Musíte odpovedať IBA v slovenčine.",
            'ta': "நீங்கள் தமிழில் மட்டும் பதில் அளிக்க வேண்டும்."
        }

        # 고정값
        custom_temperature = 0.7
        custom_prompt = celebrity.celebrity_prompt
        custom_voice_id = celebrity.celebrity_voice_id
        custom_stability = 0.3
        custom_style = 0.5
        custom_language = request.POST.get("language",'en')
        custom_speed = 1.0
        custom_model = "gpt-3.5-turbo"

        if not custom_voice_id:
            return JsonResponse({"error": "지금 voice id 가 없습니다."})

        language_instruction = language_instructions.get(custom_language, language_instructions['en'])

        system_prompt = f"""
        You are an AI that must respond strictly in the user's selected language.

        {language_instruction}

        Do not respond in English unless explicitly asked.

        {custom_prompt}
        """.strip()


        emotion_prompt = f"""
        Analyze the sentiment of the following text and respond ONLY with ONE word:
        [Happy, Sad, Neutral, Surprise, Excited, Relaxed, ]
        Text: "{user_input}"
        Emotion:
"""
        emotion_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": emotion_prompt}]
        )
        emotion = emotion_response.choices[0].message.content.strip()
        print(celebrity, custom_language,custom_voice_id, user_input)

        response = openai_client.chat.completions.create(
            model=custom_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=custom_temperature
        )
        ai_text = response.choices[0].message.content.strip()

        audio_stream = eleven_client.text_to_speech.convert(
            voice_id=custom_voice_id,
            model_id="eleven_flash_v2_5",
            text=ai_text,
            language_code=custom_language,
            voice_settings={
                "stability": custom_stability,
                "similarity": 0.75,
                "style": custom_style,
                "speed": custom_speed
            }
        )


        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
        os.makedirs(audio_dir, exist_ok=True)

        filename = f"{uuid.uuid4().hex}.mp3"
        audio_path = os.path.join(audio_dir, filename)

        with open(audio_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
        

        

        return JsonResponse({
            "ai_text": ai_text,
            "audio_url": f"/media/audio/{filename}"
        })

    return JsonResponse({"error": "Invalid request"}, status=400)
