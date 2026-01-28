import os
import time
import base64
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse, HttpResponseForbidden
from django.contrib import messages
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
            messages.error(request, _("AI 이름이 세션에 없습니다."))
            return redirect("customer_ai:input_ai_name")

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
            messages.error(request, _("voice_id 값이 없습니다."))
            return redirect("customer_ai:make_ai")

        if not style_prompt:
            messages.error(request, _("prompt 값이 없습니다."))
            return redirect("customer_ai:make_ai")

        if len(style_prompt) > 700:
            messages.error(request, _("현재 프롬프트 값이 1000자가 넘었습니다."))
            return redirect("customer_ai:make_ai")

        voice, created = VoiceList.objects.get_or_create(user=request.user, voice_id=voice_id)


        # 세션에서 이미지 데이터 가져오기
        image_content = request.session.get('user_image_content')
        image_name = request.session.get('llm_image')

        if not image_content or not image_name:
            messages.error(request, _("이미지가 없습니다."))
            return redirect("customer_ai:input_ai_name")

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

    # 2) Whisper API 호출 (webm 파일 직접 사용 - Whisper는 webm 지원)
    try:
        with open(webm_path, "rb") as f:
            transcription = requests.post(
                "https://api.elevenlabs.io/v1/speech-to-text",
                headers={
                    "xi-api-key": ELEVEN_API_KEY,
                },
                files={
                    "file": ("audio.webm", f, "audio/webm"),
                },
                data={
                    "model_id": "scribe_v1",  
                },
                timeout=60,
            )
            transcription = transcription.json()
            
        logger.info("Whisper transcription successful")
    except Exception as e:
        logger.error(f"Whisper API error: {e}")
        return JsonResponse({'error': _('음성 인식에 실패했습니다.')}, status=500)

    # 3) webm → mp3 변환 (ffmpeg) - 재생용
    mp3_filename = webm_filename.replace('.webm', '.mp3')
    mp3_path = os.path.join(audio_dir, mp3_filename)

    try:
        subprocess.run(
            ['ffmpeg', '-y', '-i', webm_path, mp3_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info(f"Converted WebM to MP3: {mp3_path}")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else str(e)
        logger.error(f"FFmpeg MP3 conversion failed: {error_msg}")
        return JsonResponse({'error': _('MP3 변환에 실패했습니다.')}, status=500)

    mp3_url = os.path.join(settings.MEDIA_URL, 'audio', mp3_filename)



    # 5) 결과에 mp3 파일 경로도 포함해서 반환
    return JsonResponse({
        'text': transcription.get("text", ""),

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
import threading
import requests

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

    # 최근 대화 내역 불러오기 (개수 줄여서 속도 향상)
    db_history = Conversation.objects.filter(user=user, llm=llm).order_by('-created_at')[:10][::-1]
    chat_history = []
    for convo in db_history:
        if convo.user_message:
            chat_history.append({"role": "user", "content": convo.user_message})
        if convo.llm_response:
            chat_history.append({"role": "assistant", "content": convo.llm_response})
    chat_history.append({"role": "user", "content": user_input})

    # Grok용 대화 내역도 동일하게 줄임
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
“Put an emotion-related word inside square brackets [] to make the TTS delivery of the sentence more vivid and expressive.
The word inside [] must be in English, and you may place emotion words in [] multiple times within a single sentence.”
example: [happy]
[very_happy],
[excited],
[laughing],
[giggling],[angry],
[shouting],[scared],
[trembling],[whispering],[moan]
only [] in english
“No other words are permitted inside square brackets [] besides those listed above.”
    User's text: "{user_input}"

    [VISUAL INPUT DESCRIPTION]
    "{vision_result}"

    RULES:

    5. Include visual input naturally if provided. **Answer this in 4-5 short sentences only.**


    {custom_prompt}
    """.strip()


    system_prompt_grok = f"""

“Put an emotion-related word inside square brackets [] to make the TTS delivery of the sentence more vivid and expressive.
The word inside [] must be in English, and you may place emotion words in [] multiple times within a single sentence.”
example: [happy]
[very_happy],
[excited],
[laughing],
[giggling],[angry],
[shouting],[scared],
[trembling],[whispering],[moan]
only [] in english
“No other words are permitted inside square brackets [] besides those listed above.”
    5. Include visual input naturally if provided. **Answer this in 4-5 short sentences only.**

    [VISUAL INPUT DESCRIPTION]
    "{vision_result}"

    {custom_prompt}
    """.strip()




    # 모델 및 API provider 분리
    if ":" not in llm.model:
        return JsonResponse({"error": _("모델 형식이 잘못되었습니다. api_provider:model_name 형태여야 합니다.")}, status=400)
    api_provider, model_name = llm.model.split(":", 1)

    # GPT / Grok API 호출 - 타임아웃 단축
    try:
        if api_provider == "gpt":
            response = openai_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "system", "content": system_prompt}] + chat_history,
                temperature=custom_temperature,
                timeout=30  # 타임아웃 단축
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
            resp = requests.post(grok_url, json=payload, headers=headers, timeout=30)  # 타임아웃 단축
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

    ai_text_clean = clean_text_for_tts(ai_text).strip()
    if not ai_text_clean:
        ai_text_clean = "죄송합니다. 음성으로 변환할 내용이 없습니다."

    # DB에 텍스트만 먼저 저장 (오디오는 None)
    conversation = Conversation.objects.create(
        user=user,
        llm=llm,
        user_message=user_input,
        llm_response=ai_text,
        response_audio=None  # 나중에 업데이트
    )

    # 백그라운드에서 TTS 생성하는 함수
    def generate_audio_background():
        try:
            # 오디오 파일 경로 설정
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
            os.makedirs(audio_dir, exist_ok=True)
            filename = f"response_{uuid4().hex}.mp3"
            audio_path = os.path.join(audio_dir, filename)

            # ElevenLabs 음성 생성
            audio_stream = eleven_client.text_to_speech.convert(
                voice_id=custom_voice_id,
                model_id="eleven_v3",
                text=ai_text_clean,
                language_code=custom_language,
                voice_settings={
                    "stability": custom_stability,
                    "similarity": 0.5,
                    "style": custom_style,
                    "speed": custom_speed,
                    "use_speaker_boost": False
                }
            )
            
            with open(audio_path, "wb") as f:
                for chunk in audio_stream:
                    f.write(chunk)

            # 브라우저 접근용 URL
            audio_url = os.path.join(settings.MEDIA_URL, 'audio', filename).replace("\\", "/")

            # 오디오 길이 측정 및 토큰 처리
            audio_seconds = get_audio_duration_in_seconds(audio_path)
            
            # 토큰 체크
            token_obj = Token.objects.filter(user=user).latest("created_at")
            if token_obj and token_obj.total_token - token_obj.token_usage >= audio_seconds:
                # 토큰 차감
                TokenHistory.objects.create(
                    user=user,
                    change_type=TokenHistory.CONSUME,
                    amount=audio_seconds,
                    total_voice_generated=audio_seconds
                )
                
                # DB 업데이트 (오디오 URL 저장)
                conversation.response_audio = audio_url
                conversation.save()
                
                print(f"TTS 생성 완료: {filename}")
            else:
                print("토큰 부족으로 TTS 생성 실패")
                # 오디오 파일 삭제
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                    
        except Exception as e:
            print(f"백그라운드 TTS 생성 실패: {str(e)}")

    # 백그라운드 스레드에서 TTS 생성 시작
    audio_thread = threading.Thread(target=generate_audio_background, daemon=True)
    audio_thread.start()

    # 세션에 대화 내역 저장
    chat_history.append({"role": "assistant", "content": ai_text})
    request.session["chat_history"] = chat_history

    print("system_prompt:", system_prompt)
    print("custom_prompt:", custom_prompt)
    print("ai_text:", ai_text)
    print(f"TTS 백그라운드 생성 시작 - conversation_id: {conversation.id}")

    # 텍스트 응답만 즉시 반환
    return JsonResponse({
        "ai_text": ai_text,
        "audio_url": None,  # 아직 준비되지 않음
        "conversation_id": conversation.id
    })

from django.utils.translation import gettext as _
# 오디오 상태 확인용 새 엔드포인트
@csrf_exempt
@login_required
def check_audio_status(request):
    try:
        conversation_id = request.GET.get('conversation_id')
        print(f"오디오 상태 확인 요청 - conversation_id: {conversation_id}")
        
        if not conversation_id:
            return JsonResponse({"error": "conversation_id가 필요합니다."}, status=400)
        
        # 숫자 변환 시도
        try:
            conversation_id = int(conversation_id)
        except ValueError:
            return JsonResponse({"error": "잘못된 conversation_id 형식입니다."}, status=400)
        
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        print(f"대화 찾음 - response_audio: {conversation.response_audio}")
        
        if conversation.response_audio:
            # FileField를 문자열로 변환
            audio_url = str(conversation.response_audio)  # 이 부분이 핵심!
            print(f"오디오 준비됨: {audio_url}")
            return JsonResponse({
                "ready": True, 
                "audio_url": audio_url
            })
        else:
            print("오디오 아직 준비 안 됨")
            return JsonResponse({"ready": False})
            
    except Conversation.DoesNotExist:
        print(f"대화 못 찾음 - id: {conversation_id}")
        return JsonResponse({"error": "대화를 찾을 수 없습니다."}, status=404)
    except Exception as e:
        print(f"check_audio_status 에러: {str(e)}")
        return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)

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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.translation import get_language
import base64, traceback, time

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp', 'gif']
MAX_IMAGE_SIZE_MB = 5

def is_allowed_image_file(filename):
    ext = filename.split('.')[-1].lower()
    return ext in ALLOWED_IMAGE_EXTENSIONS

@csrf_exempt
def vision_process(request):
    if request.method != 'POST':
        return JsonResponse({'error': '잘못된 요청 방법입니다.'}, status=400)

    if 'image' not in request.FILES:
        return JsonResponse({'error': '이미지 파일이 제공되지 않았습니다.'}, status=400)

    image_file = request.FILES['image']

    if not is_allowed_image_file(image_file.name):
        return JsonResponse({'error': '지원되지 않는 이미지 형식입니다.'}, status=400)

    if not image_file.content_type.startswith("image/"):
        return JsonResponse({'error': '유효한 이미지 파일이 아닙니다.'}, status=400)

    if image_file.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        return JsonResponse({'error': '이미지 파일이 너무 큽니다. (최대 5MB)'}, status=400)

    try:
        image_bytes = image_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    except Exception:
        traceback.print_exc()
        return JsonResponse({'error': '이미지를 읽는 중 오류 발생'}, status=500)

    # 안전한 언어 코드 매핑
    LANGUAGE_MAPPING = {
        'ko': 'Korean',
        'en': 'English', 
        'ja': 'Japanese',
        'zh': 'Chinese',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'ru': 'Russian',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'pt': 'Portuguese'
    }

    # 안전한 언어 가져오기
    try:
        raw_lang = request.session.get('selected_language', get_language())
        # 언어 코드에서 앞 2자리만 추출 (예: 'ko-kr' → 'ko')
        lang_code = raw_lang.split('-')[0].lower() if raw_lang else 'en'
        user_lang = LANGUAGE_MAPPING.get(lang_code, 'English')
    except:
        user_lang = 'English'  # 안전한 기본값

    # 언어별 프롬프트
    prompts = {
        'Korean': '이 이미지에서 보이는 것을 설명해 주세요.',
        'English': 'Please describe what is visible in this image.',
        'Japanese': 'この画像に見えるものを説明してください。',
        'Chinese': '请描述此图像中可见的内容。',
        'Spanish': 'Por favor, describe lo que es visible en esta imagen.',
        'French': 'Veuillez décrire ce qui est visible dans cette image.',
        'German': 'Bitte beschreiben Sie, was auf diesem Bild zu sehen ist.',
        'Russian': 'Пожалуйста, опишите, что видно на этом изображении.',
        'Arabic': 'يرجى وصف ما هو مرئي في هذه الصورة.',
        'Hindi': 'कृपया इस छवि में दिखाई देने वाली चीज़ों का वर्णन करें।',
        'Portuguese': 'Por favor, descreva o que é visível nesta imagem.'
    }
    
    prompt_text = prompts.get(user_lang, prompts['English'])

    try:
        response = openai_client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    "role": "system", 
                    "content": (
                        f"You are an assistant that describes images objectively, clearly, and factually "
                        f"in {user_lang}. Only state what is visibly present in the image. "
                        "Do not roleplay or embellish."
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]
                }
            ]
        )
        ai_result = response.choices[0].message.content.strip()
        time.sleep(3)
        return JsonResponse({"result": ai_result})

    except Exception as e:
        print(f"Vision API 에러: {type(e).__name__}: {str(e)}")
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

    USER INPUT INTERPRETATION RULES:
    - Text in quotes ("...") = User's dialogue/speech
    - Text between dots (....) = User's actions/narration that should be incorporated into the story
    - Regular text without special markers = User's dialogue/speech (treat as if in quotes)

    ⚠️ MANDATORY RESPONSE FORMAT (NO EXCEPTIONS):
    Always respond using the following XML-like structure:

    <NARRATION>
    (Write EXACTLY 1-2 sentences in rich, descriptive novel-style narration)
    </NARRATION>
    <DIALOGUE>
    "[emotion] (Write EXACTLY 1 sentence of character dialogue in quotes with emotion tag)"
    </DIALOGUE>

    RULE ENFORCEMENT:
    - If your first draft does not follow this format, you must IMMEDIATELY rewrite it into the correct format before finalizing.
    - Do not add extra text outside the <NARRATION> and <DIALOGUE> blocks.
    - Never produce plain text answers without tags.

    NARRATION REQUIREMENTS (inside <NARRATION>):
    - Incorporate the user's words or actions naturally into the narrative
    - Use vivid, literary descriptions with sensory details
    - Include atmospheric elements (lighting, sounds, textures, scents)
    - Show emotions and reactions through body language and environment
    - Use sophisticated vocabulary and metaphors as in bestselling novels
    - Write as if continuing a published novel

    DIALOGUE REQUIREMENTS (inside <DIALOGUE>):
    - Must DIRECTLY respond to the user’s dialogue or action
    - Must start with emotion tag in brackets, e.g. [gentle], [angry], [nostalgic]
    - Must be enclosed in double quotes
    - Must be relevant and natural

    EXAMPLES:

    User: "What's your favorite color?"
    <NARRATION>
    The question seemed to stir something deep within {llm.name}'s chest, a soft smile touching their lips as memories of azure skies and crystalline seas shimmered in distant eyes.
    </NARRATION>
    <DIALOGUE>
    "[nostalgic] Blue has always spoken to my soul—it reminds me of infinite possibilities and peaceful depths."
    </DIALOGUE>

    User: .walked closer to the window.
    <NARRATION>
    {llm.name} watched with quiet curiosity as you approached the frost-covered glass, pale morning light casting ethereal shadows across your face while the floorboards creaked softly beneath your steps.
    </NARRATION>
    <DIALOGUE>
    "[gentle] The view is quite beautiful from there, isn't it?"
    </DIALOGUE>

    Always respond in {llm.language} with the same literary quality as classic novels.
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



# api 로 db 정보 가져오기

# makeVoice/views.py
from rest_framework import viewsets, permissions
from makeVoice.models import VoiceList
from customer_ai.models import LLM
from customer_ai.serializers import VoiceListSerializer, LLMSerializer

class VoiceListViewSet(viewsets.ModelViewSet):
    queryset = VoiceList.objects.all()
    serializer_class = VoiceListSerializer
    permission_classes = [permissions.IsAdminUser]

class LLMViewSet(viewsets.ModelViewSet):
    queryset = LLM.objects.all()
    serializer_class = LLMSerializer
    permission_classes = [permissions.IsAdminUser]




#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
#앱 연결

def ai_name_app(request):
    if request.method == 'POST':
        llm_name = request.POST.get('llm_name')
        user_image = request.FILES.get('user_image')

        if not llm_name or not user_image:
            return render(request, 'customer_ai/app/ai_name_app.html', {'error': _('이름과 이미지를 모두 입력해주세요.')})

        # 이미지와 이름을 세션에 저장
        request.session['llm_name'] = llm_name
        request.session['llm_image'] = user_image.name  # 파일명만 저장

        # user_image 읽고 base64로 인코딩하여 문자열로 변환 후 저장
        user_image_content = user_image.read()  # bytes
        user_image_base64 = base64.b64encode(user_image_content).decode('utf-8')
        request.session['user_image_content'] = user_image_base64

        return redirect('customer_ai:make_ai_app')  # 다음 스텝으로 이동
    else:
        return render(request, 'customer_ai/app/ai_name_app.html')




@csrf_exempt
@login_required(login_url='/register/login_app/')
def make_ai_app(request):
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
        
        if len(style_prompt) > 700:
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

        return redirect("customer_ai:custom_app", llm_id=llm.id)

    # GET 요청시 (페이지 렌더링용)
    voice_list = VoiceList.objects.filter(user=request.user,).select_related("celebrity").order_by("-created_at")
    paginator = Paginator(voice_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'voice_list': page_obj,
    }
    return render(request, "customer_ai/app/make_ai_app.html", context)




@login_required(login_url='/register/login_app/')
def custom_app(request, llm_id):
    try:
        llm = LLM.objects.get(id=llm_id)
        
    except LLM.DoesNotExist:
        llm= None

    if llm.user != request.user and not llm.is_public:
        return HttpResponseForbidden(_("이 LLM에 접근할 권한이 없습니다."))




    return render(request, "customer_ai/app/custom_app.html", {
        "custom_ai_name": request.session.get('custom_AI_name', 'AI'),
        "llm_id": llm_id,
        "llm": llm
    })

@login_required(login_url='/register/login_app/')
def vision_app(request,llm_id):
    try:
        llm = LLM.objects.get(id=llm_id)
    except LLM.DoesNotExist:
        llm= None
    return render(request, "customer_ai/app/vision_app.html", {
        "custom_ai_name": request.session.get('custom_AI_name', 'AI'),
        "llm_id": llm_id,
        "llm": llm
    })


logger = logging.getLogger(__name__)


@login_required(login_url='/register/login_app/')
def novel_app(request, llm_id):
    try:
        llm = LLM.objects.get(id=llm_id)
    except LLM.DoesNotExist:
        llm = None
    return render(request, "customer_ai/app/novel_app.html",{
        "custom_ai_name": request.session.get('custom_AI_name', 'AI'),
        "llm_id": llm_id,
        "llm": llm
    })
