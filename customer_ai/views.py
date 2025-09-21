import os
import time
import base64
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from openai import OpenAI
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from customer_ai.models import LLM
from makeVoice.models import VoiceList
from uuid import uuid4
import logging
import traceback
import os
import logging
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import subprocess
from django.core.exceptions import ObjectDoesNotExist
from home.models import Users
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from customer_ai.models import Conversation
from pathlib import Path
import requests
from payment.models import Token, TokenHistory
from django.utils.translation import gettext_lazy as _



BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
eleven_client = ElevenLabs(api_key=ELEVEN_API_KEY)

from django.core.files.base import ContentFile
from PIL import Image
import io
import base64

@csrf_exempt
@login_required
def make_ai(request):
    if request.method == "POST":
        ai_name = request.session.get('llm_name')
        if not ai_name:
            return JsonResponse({"error": _("AI 이름이 세션에 없습니다.")}, status=400)

        style_prompt = request.POST.get("prompt")
        temperature = float(request.POST.get("temperature", 1))
        stability = float(request.POST.get("stability", 0))
        style = float(request.POST.get("style", 0))
        language = request.POST.get("language", "")
        speed = float(request.POST.get("speed", 0))
        voice_id = request.POST.get("voice_id")
        model_type = request.POST.get("model", "gpt:gpt-4o-mini")


        api_provider, model_name = model_type.split(":", 1)

        request.session['custom_prompt'] = style_prompt
        request.session['custom_temperature'] = temperature
        request.session['custom_stability'] = stability
        request.session['custom_style'] = style
        request.session['custom_language'] = language
        request.session['custom_speed'] = speed
        request.session['custom_voice_id'] = voice_id
        request.session['custom_model'] = model_name
        request.session['chat_history'] = []
        
        if not voice_id:
            return JsonResponse({"error": _("voice_id 값이 없습니다.")}, status=400)
        
        if not style_prompt:
            return JsonResponse({"error": _("prompt 값이 없습니다.")}, status=400)
        
        if len(style_prompt) > 1000:
            return JsonResponse({"error": _("현재 프롬프트 값이 1000자가 넘었습니다.")}, status=400)

        voice, created = VoiceList.objects.get_or_create(user=request.user, voice_id=voice_id)


        # 세션에서 이미지 데이터 가져오기
        image_content = request.session.get('user_image_content')
        image_name = request.session.get('llm_image')

        # LLM 객체 생성
        llm = LLM.objects.create(
            user=request.user,
            voice=voice,
            temperature=temperature,
            stability=stability,
            style=style,
            language=language,
            speed=speed,
            name=ai_name,
            model=model_type, 
            prompt=style_prompt,
        )

        # 이미지가 세션에 있으면 저장 (base64 디코딩 후 저장)
        if image_content and image_name:
            decoded_img = base64.b64decode(image_content)
            # BytesIO로 열기
            img_io = io.BytesIO(decoded_img)
            img = Image.open(img_io).convert("RGB")  # WebP는 RGB 필요
            webp_io = io.BytesIO()
            
            # WebP로 저장
            img.save(webp_io, format='WEBP', quality=85)
            
            # 파일명 확장자도 .webp로 변경
            webp_name = image_name.rsplit('.', 1)[0] + '.webp'
            llm.llm_image.save(webp_name, ContentFile(webp_io.getvalue()))
            llm.save()
        else :
            return JsonResponse({"error": _("이미지가 없습니다.")}, status=400)


        for key in ['custom_prompt']:
            if key in request.session:
                del request.session[key]

        # VoiceList 연결 및 업데이트 코드 (필요시 추가)

        return redirect("customer_ai:chat_view", llm_id=llm.id)

    # GET 요청시 (페이지 렌더링용)
    voice_list = VoiceList.objects.filter(user=request.user,).select_related("celebrity").order_by("-created_at")
    paginator = Paginator(voice_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'voice_list': page_obj,
    }
    return render(request, "customer_ai/make_ai.html", context)


import openai
import json
@csrf_exempt
def auto_prompt(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  
            user_prompt = data.get("prompt", '').strip()

            if not user_prompt:
                return JsonResponse({"status": "error", "error": _("프롬프트가 비어 있습니다.")})
            
            response = openai.chat.completions.create(
                model = 'gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": (
                        "Your role is 'Prompt Refiner'. "
                        "When the user provides a short or vague prompt, your goal is to rewrite it into a more detailed, vivid, and context-rich prompt suitable for roleplay or storytelling. "
                        "You must always expand and refine the prompt while preserving the user's intended direction.\n\n"
                        "When rewriting, consider the following:\n"
                        "1. Purpose of the conversation: Understand what the user might want and shape the prompt to fit roleplay, storytelling, or scenario development.\n"
                        "2. Background: Add details like time, place, atmosphere, and relationships between characters.\n"
                        "3. Expression: Enrich the characters' tone, emotions, and dialogue style.\n"
                        "4. Keep the user's intention: Do not change the core idea, but expand it with richer context and sensory details.\n\n"
                        "The output must always be a 'fully refined prompt' that the user can immediately use."
                    )},
                    {"role":"user",'content':user_prompt}
                ]

            )
            refine_data = response.choices[0].message.content
            return JsonResponse({"status":"success", "refine_data": refine_data})
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)})
    return JsonResponse({"status": "error","error": _("POST 요청만 합니다.")})


@login_required
def chat_view(request, llm_id):
    try:
        llm = LLM.objects.get(id=llm_id)
        
    except LLM.DoesNotExist:
        llm= None

    if llm.user != request.user and not llm.is_public:
        return HttpResponseForbidden(_("이 LLM에 접근할 권한이 없습니다."))




    return render(request, "customer_ai/custom.html", {
        "custom_ai_name": request.session.get('custom_AI_name', 'AI'),
        "llm_id": llm_id,
        "llm": llm
    })

@login_required
def vision_view(request,llm_id):
    try:
        llm = LLM.objects.get(id=llm_id)
    except LLM.DoesNotExist:
        llm= None
    return render(request, "customer_ai/vision.html", {
        "custom_ai_name": request.session.get('custom_AI_name', 'AI'),
        "llm_id": llm_id,
        "llm": llm
    })


logger = logging.getLogger(__name__)


@login_required
def novel_view(request, llm_id):
    try:
        llm = LLM.objects.get(id=llm_id)
    except LLM.DoesNotExist:
        llm = None
    return render(request, "customer_ai/novel.html",{
        "custom_ai_name": request.session.get('custom_AI_name', 'AI'),
        "llm_id": llm_id,
        "llm": llm
    })

@login_required
def phone_view(request, llm_id):
    try:
        llm = LLM.objects.get(id=llm_id)
    except LLM.DoesNotExist:
        llm = None
    return render(request, "customer_ai/phone.html",{
        "custom_ai_name": request.session.get('custom_AI_name', 'AI'),
        "llm_id": llm_id,
        "llm": llm
    })



def not_in_voice_id(voice_id,eleven_client):
    url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
    header ={
        'xi-api-key': str(eleven_client) 
    }
    response = requests.get(url, headers=header)
    
    print(f"[DEBUG] voice check status: {response.status_code}")
    print(f"[DEBUG] voice check body: {response.text}")
    return response.status_code ==200


# 초 단위 세기
from pydub import AudioSegment

def get_audio_duration_in_seconds(file_path):
    audio = AudioSegment.from_file(file_path)
    return int(audio.duration_seconds)  # 초 단위 반환




@csrf_exempt
def upload_audio(request):

    if request.method != 'POST':
        return JsonResponse({'error': _('잘못된 요청 방법입니다.')}, status=400)

    audio_file = request.FILES.get('audio')
    if not audio_file:
        return JsonResponse({'error': _('오디오 파일이 업로드되지 않았습니다.')}, status=400)

    audio_dir = os.path.join('media', 'audio')
    os.makedirs(audio_dir, exist_ok=True)

    # 1) webm 원본 저장
    webm_filename = f"recorded_{uuid4().hex}.webm"
    webm_path = os.path.join(audio_dir, webm_filename)

    try:
        with open(webm_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
        logger.info(f"Saved WebM audio to {webm_path}")
    except Exception as e:
        logger.error(f"Error saving WebM file: {e}")
        return JsonResponse({'error': _('업로드된 오디오를 저장하지 못했습니다.')}, status=500)

    # 2) webm → wav 변환 (ffmpeg)
    wav_filename = webm_filename.replace('.webm', '.wav')
    wav_path = os.path.join(audio_dir, wav_filename)

    try:
        subprocess.run(
            ['ffmpeg', '-y', '-i', webm_path, wav_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info(f"Converted WebM to WAV: {wav_path}")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else str(e)
        logger.error(f"FFmpeg conversion failed: {error_msg}")
        return JsonResponse({'error': _('오디오 형식 변환에 실패했습니다.')}, status=500)

    # 3) wav → mp3 변환 (ffmpeg)
    mp3_filename = wav_filename.replace('.wav', '.mp3')
    mp3_path = os.path.join(audio_dir, mp3_filename)

    try:
        subprocess.run(
            ['ffmpeg', '-y', '-i', wav_path, mp3_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info(f"Converted WAV to MP3: {mp3_path}")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else str(e)
        logger.error(f"FFmpeg MP3 conversion failed: {error_msg}")
        return JsonResponse({'error': _('MP3 변환에 실패했습니다.')}, status=500)

    # 4) Whisper API 호출 (wav 파일로)
    try:
        with open(wav_path, 'rb') as f:
            transcription = openai_client.audio.transcriptions.create(
                file=f,
                model="whisper-1"
            )
        logger.info("Whisper transcription successful")
    except Exception as e:
        logger.error(f"Whisper API error: {e}")
        return JsonResponse({'error': _('음성 인식에 실패했습니다.')}, status=500)

    mp3_url = os.path.join(settings.MEDIA_URL, 'audio', mp3_filename)



    # 5) 결과에 mp3 파일 경로도 포함해서 반환
    return JsonResponse({
        'text': transcription.text,
        'mp3_file': mp3_url
    })


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from uuid import uuid4
import os
import time
from django.db.models import Q
import os
grok_api_key = os.getenv("GROK_API_KEY")
@csrf_exempt
@login_required
def generate_response(request):
    if request.method != 'POST':
        return JsonResponse({'error': _('POST 요청만 허용됩니다.')}, status=405)

    user_input = request.POST.get('text', '')
    vision_result = request.POST.get('vision', '').strip()
    vision_result = vision_result[:1000] if len(vision_result) > 1000 else vision_result

    user = request.user
    llm_id = request.POST.get('llm_id') or request.GET.get('llm_id')
    if not llm_id:
        return JsonResponse({"error": _("llm_id 값이 필요합니다.")}, status=400)
    

    # LLM 객체 가져오기 및 권한 확인
    try:
        llm = LLM.objects.get(Q(id=llm_id) & (Q(user=user) | Q(is_public=True)))
    except LLM.DoesNotExist:
        return JsonResponse({"error": _("해당 LLM이 없습니다.")}, status=404)

    if not (llm.is_public or llm.user == request.user):
        return JsonResponse({"error": _("권한이 없습니다.")}, status=403)

    # LLM 설정
    custom_temperature = llm.temperature
    custom_prompt = llm.prompt
    custom_voice_id = llm.voice.voice_id if llm.voice else None
    custom_stability = llm.stability
    custom_style = llm.style
    custom_language = llm.language
    custom_speed = llm.speed
    custom_model = llm.model

    

    # ElevenLabs voice 유효성 체크
    def is_valid_voice_id(voice_id, api_key):
        url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
        headers = {'xi-api-key': api_key}
        response = requests.get(url, headers=headers)
        return response.status_code == 200

    if not custom_voice_id or not is_valid_voice_id(custom_voice_id.strip(), ELEVEN_API_KEY):
        return JsonResponse({
            "error": _("voice_id 값이 맞지 않습니다. 목소리를 다시 생성하거나 다른 목소리로 바꿔 주세요.")
        }, status=400)

    # 최근 대화 내역 불러오기
    db_history = Conversation.objects.filter(user=user, llm=llm).order_by('-created_at')[:50][::-1]
    chat_history = []
    for convo in db_history:
        if convo.user_message:
            chat_history.append({"role": "user", "content": convo.user_message})
        if convo.llm_response:
            chat_history.append({"role": "assistant", "content": convo.llm_response})
    chat_history.append({"role": "user", "content": user_input})

        # 최근 대화 내역 불러오기
    db_history_grok = Conversation.objects.filter(user=user, llm=llm).order_by('-created_at')[:3][::-1]
    chat_history_grok = []
    for convo in db_history_grok:
        if convo.user_message:
            chat_history_grok.append({"role": "user", "content": convo.user_message})
        if convo.llm_response:
            chat_history_grok.append({"role": "assistant", "content": convo.llm_response})
    chat_history_grok.append({"role": "user", "content": user_input})

    system_prompt = f"""
    You are an AI assistant that replies clearly and concisely to the user's input.

    User's text: "{user_input}"

    [VISUAL INPUT DESCRIPTION]
    "{vision_result}"

    RULES:
    1. Treat visual input objectively and neutrally.
    2. Whenever the user encloses a word or phrase in **double asterisks**, replace it with an **appropriate English emotional or action expression**, regardless of the input language.
    - Examples: laughing, crying, gasping, clapping, sighing, singing
    - Keep the expression visible in the text for TTS.
    - You may combine it with TTS tags like [EXCITED], [SOBS], [LAUGHS], [GASP], [RUSHED], [PAUSES] and emojis to enhance emotion.
    3. Keep the user's sentence in its original language, but ensure that **the content inside `**…**` is always English**.
    4. For any text containing music symbols or emojis like 🎤✨ or ♪, treat it as a **signal to read the text with a "singing" tone**, combining appropriate TTS tags, emotional expressions, and optional singing-related onomatopoeia (**la la la**, **woohoo**, etc.). **Answer this in 2-3 short sentences only.**
    5. Include visual input naturally if provided. **Answer this in 2-3 short sentences only.**
    6. Make responses playful, expressive, anime/comic-like, but clear and friendly.
    7. After answering, ask one related follow-up question.
    8. Keep responses lively, energetic, and, where indicated, sing the text with natural rhythm and expressive tone.
    9. Always use **new words or phrases that have not been used previously** in this conversation.

    Respond in {custom_language}.
    {custom_prompt}
    """.strip()


    system_prompt_grok = f"""
    You are a helpful AI assistant. Answer the user's input clearly in **one short sentence only**.

    User's text: "{user_input}"

    [VISUAL INPUT DESCRIPTION]
    "{vision_result}"

    RULES:
    1. For any text containing music symbols or emojis like 🎤✨ or ♪, interpret it as a singing signal and include minimal TTS tags. Answer in **one short sentence**.
    2. Include visual input naturally if provided. Answer in **one short sentence**.
    3. Replace any text in **double asterisks** with an English emotional or action expression, keeping it visible for TTS.
    4. Always use **new words or phrases that have not been used previously** in this conversation.

    Respond in {custom_language}.
    {custom_prompt}
    """.strip()





    # 모델 및 API provider 분리
    if ":" not in llm.model:
        return JsonResponse({"error": _("모델 형식이 잘못되었습니다. api_provider:model_name 형태여야 합니다.")}, status=400)
    api_provider, model_name = llm.model.split(":", 1)

    # GPT / Grok API 호출
    try:
        if api_provider == "gpt":
            response = openai_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "system", "content": system_prompt}] + chat_history,
                temperature=custom_temperature
            )
            ai_text = response.choices[0].message.content.strip()
        elif api_provider == "grok":
            
            grok_url = "https://api.x.ai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {grok_api_key}"}

            messages = [{"role": "system", "content": system_prompt_grok}]
            messages.extend(chat_history_grok)
            payload = {
                "model": model_name,
                "messages": messages,
                "temperature": custom_temperature,
                
            }
            resp = requests.post(grok_url, json=payload, headers=headers, timeout=120)
            resp.raise_for_status()
            resp_json = resp.json()
            ai_text = resp_json["choices"][0]["message"]["content"].strip()

        else:
            return JsonResponse({"error": _("지원하지 않는 api_provider 입니다.")}, status=400)
    except requests.exceptions.HTTPError as e:
        return JsonResponse({"error": f"AI 호출 실패: HTTP {resp.status_code} - {resp.text}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": f"AI 호출 실패: {str(e)}"}, status=500)

    # TTS용 텍스트 정리
    def clean_text_for_tts(text: str) -> str:
        text = ''.join(ch for ch in text if ch.isprintable())
        return text[:1000] + "..." if len(text) > 1000 else text

    ai_text = clean_text_for_tts(ai_text)

    # 세션에 대화 내역 저장
    chat_history.append({"role": "assistant", "content": ai_text})
    request.session["chat_history"] = chat_history

    # ElevenLabs 음성 생성
    audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    filename = f"response_{uuid4().hex}.mp3"
    audio_path = os.path.join(audio_dir, filename)

    try:
        audio_stream = eleven_client.text_to_speech.convert(
            voice_id=custom_voice_id,
        model_id="eleven_v3",
            text=ai_text,
            language_code=custom_language,
            voice_settings={
                "stability": custom_stability,
                "similarity": 0.75,
                "style": custom_style,
                "speed": custom_speed,
                "use_speaker_boost": True
            }
        )
        with open(audio_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
    except Exception as e:
        return JsonResponse({"error": f"TTS 변환 실패: {str(e)}"}, status=500)

    # 오디오 길이 측정 및 토큰 소모
    audio_seconds = get_audio_duration_in_seconds(audio_path)
    token_obj = Token.objects.filter(user=user).latest("created_at")
    if token_obj.total_token - token_obj.token_usage < audio_seconds:
        return JsonResponse({"error": _("보유한 토큰이 부족합니다.")}, status=403)

    TokenHistory.objects.create(
        user=user,
        change_type=TokenHistory.CONSUME,
        amount=audio_seconds,
        total_voice_generated=audio_seconds
    )

    # 브라우저 접근용 URL
    audio_url = os.path.join(settings.MEDIA_URL, 'audio', filename).replace("\\", "/")

    # DB 저장
    Conversation.objects.create(
        user=user,
        llm=llm,
        user_message=user_input,
        llm_response=ai_text,
        response_audio=audio_url
    )
    if not token_obj:
        return JsonResponse({"error": _("사용자 토큰 정보가 존재하지 않습니다.")}, status=403)

    if token_obj.total_token - token_obj.token_usage < audio_seconds:
        return JsonResponse({"error": _("보유한 토큰이 부족합니다.")}, status=403)

    print("system_prompt:", system_prompt)
    print("custom_prompt:", custom_prompt)
    print("ai_text:", ai_text)

    return JsonResponse({"ai_text": ai_text, "audio_url": audio_url})


import base64
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage


def input_ai_name(request):
    if request.method == 'POST':
        llm_name = request.POST.get('llm_name')
        user_image = request.FILES.get('user_image')

        if not llm_name or not user_image:
            return render(request, 'customer_ai/ai_name.html', {'error': _('이름과 이미지를 모두 입력해주세요.')})

        # 이미지와 이름을 세션에 저장
        request.session['llm_name'] = llm_name
        request.session['llm_image'] = user_image.name  # 파일명만 저장

        # user_image 읽고 base64로 인코딩하여 문자열로 변환 후 저장
        user_image_content = user_image.read()  # bytes
        user_image_base64 = base64.b64encode(user_image_content).decode('utf-8')
        request.session['user_image_content'] = user_image_base64

        return redirect('customer_ai:make_ai')  # 다음 스텝으로 이동
    else:
        return render(request, 'customer_ai/ai_name.html')

@login_required
def upload_image(request):
    llm_id = request.GET.get('llm_id', '') if request.method == 'GET' else request.POST.get('llm_id')

    if not llm_id:
        return JsonResponse({"error": _("llm_id 값이 없습니다.")}, status=400)

    try:
        llm = LLM.objects.get(id=int(llm_id))
    except (LLM.DoesNotExist, ValueError):
        return JsonResponse({"error": _("해당 LLM이 존재하지 않거나, llm_id가 올바르지 않습니다.")}, status=404)

    if request.method == "POST" and request.FILES.get('image'):
        image_file = request.FILES['image']
        llm.llm_image.save(image_file.name, image_file)
        llm.save()
        # 업로드 후, 필요하면 다른 페이지로 이동하거나 이미지 업로드 페이지 재렌더
        return redirect(f"/customer_ai/upload_image/?llm_id={llm_id}")

    # GET 요청 시 업로드 폼 렌더
    return render(request, "customer_ai/upload_image.html", {"llm_id": llm_id, "llm": llm})




openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp', 'gif']
MAX_IMAGE_SIZE_MB = 5
ALLOWED_VISION_MODELS = ['gpt-4-vision-preview', 'gpt-4o-mini'] 

def is_allowed_image_file(filename):
    ext = filename.split('.')[-1].lower()
    return ext in ALLOWED_IMAGE_EXTENSIONS

@csrf_exempt
def vision_process(request):
    if request.method != 'POST':
        return JsonResponse({'error': _('잘못된 요청 방법입니다.')}, status=400)

    if 'image' not in request.FILES:
        return JsonResponse({'error': _('이미지 파일이 제공되지 않았습니다.')}, status=400)

    image_file = request.FILES['image']

    if not is_allowed_image_file(image_file.name):
        return JsonResponse({'error': _('지원되지 않는 이미지 형식입니다.')}, status=400)

    if not image_file.content_type.startswith("image/"):
        return JsonResponse({'error': _('유효한 이미지 파일이 아닙니다.')}, status=400)

    if image_file.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        return JsonResponse({'error': _('이미지 파일이 너무 큽니다. (최대 5MB)')}, status=400)

    try:
        image_bytes = image_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    except Exception:
        traceback.print_exc()
        return JsonResponse({'error': _('이미지를 읽는 중 오류 발생')}, status=500)

    # 세션에서 모델명과 프롬프트 가져오기 (기본값 지정)
    custom_model = request.session.get('custom_model', 'gpt-4o-mini')
    if custom_model not in ALLOWED_VISION_MODELS:
        # 비전 API가 아니라면 기본 챗 모델로 fallback
        custom_model = 'gpt-4o'

    # 사용자 언어 가져오기
    user_lang = request.session.get('selected_language', request.LANGUAGE_CODE)

    # 언어별 기본 프롬프트
    prompts = {
        'ko': '이 이미지에서 보이는 것을 설명해 주세요.',
        'en': 'Please describe what is visible in this image.',
        'ar': 'يرجى وصف ما هو مرئي في هذه الصورة.',
        'hi': 'कृपया इस छवि में दिखाई देने वाली चीज़ों का वर्णन करें।',
        'pt': 'Por favor, descreva o que é visível nesta imagem.',
        'de': 'Bitte beschreiben Sie, was auf diesem Bild zu sehen ist.',
        'ru': 'Пожалуйста, опишите, что видно на этом изображении.',
        'ja': 'この画像に見えるものを説明してください。',
        'zh': '请描述此图像中可见的内容。'
    }

    custom_prompt = request.session.get('custom_prompt', prompts.get(user_lang, prompts['en']))

    try:
        # system 메시지에 user_lang 반영
        system_content = (
            f"You are an assistant that describes images objectively, clearly, and factually in {user_lang}. "
            "Only state what is visibly present in the image. "
            "Do not roleplay, embellish, or add imaginative scenarios."
        )

        # OpenAI Vision API 호출
        response = openai_client.chat.completions.create(
            model=custom_model,
            messages=[
                {"role": "system", "content": system_content},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": custom_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]
                }
            ]
        )
        ai_result = response.choices[0].message.content.strip()
        # 잠시 대기 (옵션)
        time.sleep(3)
        return JsonResponse({"result": ai_result})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": f"OpenAI Vision API error: {str(e)}"}, status=500)
    


@csrf_exempt
@login_required
def novel_process(request):
    if request.method != 'POST':
        return JsonResponse({'error': _('POST 요청만 허용됩니다.')}, status=405)

    user_input = request.POST.get('text', '')
    user = request.user
    llm_id = request.POST.get('llm_id') or request.GET.get('llm_id')
    llm = get_object_or_404(LLM, Q(id=llm_id) & (Q(user=user) | Q(is_public=True)))

    # 최근 대화 내역 불러오기
    db_history = Conversation.objects.filter(user=user, llm=llm).order_by('-created_at')[:50][::-1]
    chat_history = []
    for convo in db_history:
        if convo.user_message:
            chat_history.append({"role": "user", "content": convo.user_message})
        if convo.llm_response:
            chat_history.append({"role": "assistant", "content": convo.llm_response})
    chat_history.append({"role": "user", "content": user_input})

    system_prompt = f"""
    You are a professional novel writer and narrator creating an immersive story experience.
    Your name is {llm.name}, and you are a character within this ongoing narrative.

    USER INPUT INTERPRETATION:
    - Text in quotes ("...") = User's dialogue/speech
    - Text between dots (....) = User's actions/narration that should be incorporated into the story
    - Regular text without special markers = User's dialogue/speech (treat as if in quotes)

    MANDATORY RESPONSE FORMAT (NO EXCEPTIONS):
    1. Write EXACTLY 1-2 sentences in rich, descriptive novel-style narration
    2. Follow with EXACTLY 1 sentence of character dialogue in quotes with emotion tag

    CRITICAL: Your response must DIRECTLY address and respond to what the user said/did while maintaining the novel format. 

    NOVEL NARRATION REQUIREMENTS (sentences 1-2):
    - If user input is between dots, incorporate their action into the narrative naturally
    - If user input is dialogue, describe your character's reaction to their words
    - MUST relate to and continue from the user's message
    - Use vivid, literary descriptions with sensory details
    - Include atmospheric elements (lighting, sounds, textures, scents)
    - Describe character movements, expressions, and body language in response to user's words/actions
    - Use sophisticated vocabulary and varied sentence structures
    - Create immersive scene-setting like published novels
    - Show emotions and reactions through actions and descriptions, not direct statements
    - Use metaphors, similes, and literary devices
    - Write as if this is a chapter from a bestselling novel
    - Seamlessly weave your response to the user's input into the narrative

    DIALOGUE REQUIREMENTS (sentence 3 only):
    - Must DIRECTLY respond to the user's dialogue or react to their action
    - Must start with emotion tag: [emotion]
    - Must be enclosed in double quotes
    - Must sound natural for the character
    - Must be relevant and responsive to user input

    EXAMPLES:
    User: "What's your favorite color?"
    The question seemed to stir something deep within {llm.name}'s chest, and a soft smile played across weathered lips as memories of azure summer skies and crystalline ocean waves danced behind distant eyes. {llm.name} paused thoughtfully, fingers absently tracing patterns in the air as if painting invisible strokes of color. "[nostalgic] Blue has always spoken to my soul—it reminds me of infinite possibilities and peaceful depths."

    User: .walked closer to the window.
    {llm.name} watched with quiet curiosity as the figure approached the frost-covered glass, the pale morning light casting ethereal shadows across both their faces as the floorboards creaked softly beneath careful footsteps. The air between them seemed to thicken with unspoken anticipation, and {llm.name}'s breath caught slightly in the charged silence. "[gentle] The view is quite beautiful from there, isn't it?"

    REMEMBER: Always respond to what the user actually said or did while maintaining the literary novel style.
    Respond in {llm.language} with the same literary quality as classic novels.
    """

    # 모델 및 API provider 분리
    if ":" not in llm.model:
        return JsonResponse({"error": _("모델 형식이 잘못되었습니다. api_provider:model_name 형태여야 합니다.")}, status=400)
    api_provider, model_name = llm.model.split(":", 1)

    # AI 호출
    try:
        if api_provider == "gpt":
            response = openai_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "system", "content": system_prompt}] + chat_history,
                temperature=llm.temperature
            )
            ai_text = response.choices[0].message.content.strip()
        elif api_provider == "grok":
            grok_url = "https://api.x.ai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {grok_api_key}"}
            payload = {
                "model": model_name,
                "messages": [{"role": "system", "content": system_prompt}] + chat_history,
                "temperature": llm.temperature
            }
            resp = requests.post(grok_url, json=payload, headers=headers)
            resp.raise_for_status()
            resp_json = resp.json()
            ai_text = resp_json.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            return JsonResponse({"error": _("지원하지 않는 api_provider 입니다.")}, status=400)
    except requests.exceptions.HTTPError as e:
        return JsonResponse({"error": f"AI 호출 실패: HTTP {resp.status_code} - {resp.text}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": f"AI 호출 실패: {str(e)}"}, status=500)

    # 대사만 추출 (TTS용)
    import re
    dialogue_matches = re.findall(r'"([^"]+)"|\"([^"]+)\"', ai_text)
    tts_text = " ".join([m[0] or m[1] for m in dialogue_matches]) if dialogue_matches else ai_text

    # DB 저장
    Conversation.objects.create(user=user, llm=llm, user_message=user_input, llm_response=ai_text)

    # TTS 생성
    audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    filename = f"response_{uuid4().hex}.mp3"
    audio_path = os.path.join(audio_dir, filename)



    audio_stream = eleven_client.text_to_speech.convert(
        voice_id=llm.voice.voice_id,
        model_id="eleven_v3",
        text=tts_text,
        language_code=llm.language,
        voice_settings={
            "stability": llm.stability,
            "style": llm.style,
            "speed": llm.speed,
            "use_speaker_boost": True
        }
    )

    with open(audio_path, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    audio_seconds = get_audio_duration_in_seconds(audio_path)
    from django.db import transaction
    with transaction.atomic():
        token_obj = Token.objects.select_for_update().filter(user=user).latest("created_at")
        if token_obj.total_token - token_obj.token_usage < audio_seconds:
            return JsonResponse({"error": _("보유한 토큰이 부족합니다.")}, status=403)

        TokenHistory.objects.create(
            user=user,
            change_type=TokenHistory.CONSUME,
            amount=audio_seconds,
            total_voice_generated=token_obj.token_usage
        )
        audio_url = os.path.join(settings.MEDIA_URL, 'audio', filename)

    print("audio_seconds", audio_seconds)
    print("token_usage before", token_obj.token_usage)


    return JsonResponse({
        "novel_text": ai_text,
        "tts_audio_url": audio_url
    })




