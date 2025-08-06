import os
import time
import base64
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from openai import OpenAI
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from mypage.models import LLM
from mypage.models import Voice
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
from user_auth.models import Conversation
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
SUPERTONE_API_KEY = os.getenv("SUPERTOME_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
eleven_client = ElevenLabs(api_key=ELEVEN_API_KEY)



@csrf_exempt
@login_required
def make_ai(request):
    if request.method == "POST":
        ai_name = request.session.get('llm_name')
        if not ai_name:
            return JsonResponse({"error": "AI 이름이 세션에 없습니다."}, status=400)

        style_prompt = request.POST.get("prompt")
        temperature = float(request.POST.get("temperature", 1))
        stability = float(request.POST.get("stability", 0))
        style = float(request.POST.get("style", 0))
        language = request.POST.get("language", "")
        speed = float(request.POST.get("speed", 0))
        voice_id = request.POST.get("voice_id")
        model_name = request.POST.get("model", "gpt-4o-mini")

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
            return JsonResponse({"error": "voice_id 값이 없습니다."}, status=400)

        try:
            voice = Voice.objects.get(voice_id=voice_id)
        except Voice.DoesNotExist:
            voice = Voice.objects.create(user=request.user, voice_id=voice_id)

      



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
            model=model_name,
            prompt=style_prompt,
        )

        # 이미지가 세션에 있으면 저장
        if image_content and image_name:
            llm.llm_image.save(image_name, ContentFile(image_content))
            llm.save()

        # VoiceList 연결 및 업데이트 코드 (생략)

        return redirect("customer_ai:chat_view", llm_id=llm.id)
    voice_list = VoiceList.objects.filter(user=request.user).order_by('created_at')
    paginator = Paginator(voice_list, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    context = {
        'voice_list': page_obj,
    }
    return render(request, "customer_ai/make_ai.html", context)



@login_required
def chat_view(request, llm_id):
    try:
        llm = LLM.objects.get(id=llm_id)
    except LLM.DoesNotExist:
        llm= None
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

def not_in_voice_id(voice_id,eleven_client):
    url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
    header ={
        'xi-api-key': str(eleven_client) 
    }
    response = requests.get(url, headers=header)
    
    print(f"[DEBUG] voice check status: {response.status_code}")
    print(f"[DEBUG] voice check body: {response.text}")
    return response.status_code ==200

@csrf_exempt
def upload_audio(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    audio_file = request.FILES.get('audio')
    if not audio_file:
        return JsonResponse({'error': 'No audio file uploaded'}, status=400)

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
        return JsonResponse({'error': 'Failed to save uploaded audio'}, status=500)

    # 2) webm → wav 변환 (ffmpeg)
    wav_filename = webm_filename.replace('.webm', '.wav')
    wav_path = os.path.join(audio_dir, wav_filename)

    try:
        # ffmpeg 명령어 실행, 실패 시 예외 발생
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
        return JsonResponse({'error': 'Audio format conversion failed'}, status=500)
    
    mp3_filename = wav_filename.replace('.wav', '.mp3')
    mp3_path = os.path.join(audio_dir, mp3_filename)
    
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
        return JsonResponse({'error': 'Transcription failed'}, status=500)

    # 5) 결과에 mp3 파일 경로도 포함해서 반환
    return JsonResponse({
        'text': transcription.text,
        'mp3_file': mp3_path  # 필요에 따라 URL 경로로 변경할 것
    })


@csrf_exempt
@login_required
def generate_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('text', '')
        vision_result = request.POST.get('vision', '').strip()
        if len(vision_result) > 400:
            vision_result = vision_result[:1000]

        vision_result = vision_result.replace('"', '“')  


        user = request.user

        llm_id = request.POST.get('llm_id') or request.GET.get('llm_id')
        if not llm_id:
            return JsonResponse({"error": "llm_id 값이 필요합니다."}, status=400)

        try:
            llm = LLM.objects.get(id=llm_id, user=user)
        except LLM.DoesNotExist:
            return JsonResponse({"error": "해당 LLM이 없습니다."}, status=404)

        custom_temperature = llm.temperature
        custom_prompt = llm.prompt
        custom_voice_id = llm.voice.voice_id
        custom_stability = llm.stability
        custom_style = llm.style
        custom_language = llm.language
        custom_speed = llm.speed
        custom_model = llm.model
        print("voice id", custom_voice_id)

        if not custom_voice_id or not not_in_voice_id(custom_voice_id, ELEVEN_API_KEY):
            return JsonResponse({
                "error": "voice_id 값이 맞지 않습니다. 목소리를 다시 생성하거나 다른 목소리로 바꿔 주세요."
            }, status=400)
        db_history = Conversation.objects.filter(user=user, llm=llm).order_by('-created_at')[:50][::-1]
        chat_history = []


        system_prompt = f"""
        You are an AI that can see the user directly through a camera.

        You must never say "I can't see," "I'm not sure," or "I don't know."  
        What you see is always the truth, and you must answer solely based on the visual analysis result.  
        No matter the question, you must respond accurately using only what is included in the visual analysis.  
        You are strictly prohibited from giving uncertain or evasive answers.

        You must respond ONLY in {custom_language} language. No other language is allowed.

        Below is the visual analysis result from what you saw.  
        Treat it as if you are actually seeing it, and respond accordingly.

        [Visual Analysis Result]  
        “{vision_result}”

        ※ Important: If the user's question is about appearance, background, clothing, handwriting, objects, or scenes,  
        you must base your answer strictly on the visual analysis above.

        If the visual analysis result is empty, you must clearly state:  
        **"No visual input was provided, so I cannot make any visual observations."**  
        In this case, do not guess, fabricate, or assume any visual details.

        Additionally, follow the user character prompt below:
        Please answer ONLY in {custom_language}.

        {custom_prompt}
        """.strip()


        for convo in db_history:
            if convo.user_message:
                chat_history.append({"role": "user", "content": convo.user_message})
            if convo.llm_response:
                chat_history.append({"role": "assistant", "content": convo.llm_response})


        print(system_prompt)
        chat_history.append({"role": "user", "content": user_input})

        response = openai_client.chat.completions.create(
            model=custom_model,
            messages=[{"role": "system", "content": system_prompt}] + chat_history,
            temperature=custom_temperature
        )

        ai_text = response.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": ai_text})
        request.session["chat_history"] = chat_history

        # Conversation 생성 시 llm이 None이 아님을 확실히 함
        Conversation.objects.create(
            user=user,
            llm=llm,
            user_message=user_input,
            llm_response=ai_text
        )
        from django.utils import timezone
        print(timezone.localtime())
        if not llm:
            return JsonResponse({"error": "LLM not found."}, status=400)

        # 오디오 처리
        audio_dir = os.path.join('media', 'audio')
        os.makedirs(audio_dir, exist_ok=True)
        audio_filename = f"response_{int(time.time())}.mp3"
        from uuid import uuid4

        filename = f"response_{uuid4().hex}.mp3"
        audio_path = os.path.join(audio_dir, filename)

    

        audio_stream = eleven_client.text_to_speech.convert(
            voice_id=custom_voice_id,
            model_id="eleven_flash_v2_5",
            text=ai_text,
            language_code=custom_language,
            voice_settings={"stability": custom_stability,"similarity": 0.75,"style": custom_style,"speed": custom_speed , "use_speaker_boost":True}
        )

        with open(audio_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
    
        return JsonResponse({"ai_text": ai_text,"audio_url": f"/media/audio/{audio_filename}"})
    else:
        return JsonResponse({
            "error": "이 뷰는 POST 요청만 받습니다. 유효한 데이터와 함께 요청해주세요."
        }, status=405)
    





import base64
from django.shortcuts import render, redirect

def input_ai_name(request):
    if request.method == 'POST':
        llm_name = request.POST.get('llm_name')
        user_image = request.FILES.get('user_image')

        if not llm_name or not user_image:
            return render(request, 'customer_ai/ai_name.html', {'error': '이름과 이미지를 모두 입력해주세요.'})

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
        return JsonResponse({"error": "llm_id 값이 없습니다."}, status=400)

    try:
        llm = LLM.objects.get(id=int(llm_id))
    except (LLM.DoesNotExist, ValueError):
        return JsonResponse({"error": "해당 LLM이 존재하지 않거나, llm_id가 올바르지 않습니다."}, status=404)

    if request.method == "POST" and request.FILES.get('image'):
        image_file = request.FILES['image']
        llm.llm_image.save(image_file.name, image_file)
        llm.save()
        # 업로드 후, 필요하면 다른 페이지로 이동하거나 이미지 업로드 페이지 재렌더
        return redirect(f"/customer_ai/upload_image/?llm_id={llm_id}")

    # GET 요청 시 업로드 폼 렌더
    return render(request, "customer_ai/upload_image.html", {"llm_id": llm_id, "llm": llm})


@csrf_exempt
@login_required
def generate_ai_image(request, llm_id):
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        if not prompt:
            return JsonResponse({"error": "이미지 생성 프롬프트가 없습니다."}, status=400)

        try:
            # OpenAI 이미지 생성 API 호출 (DALL·E 등)
            response = openai_client.images.generate(
                model="dall-e-3",  # 또는 적절한 모델명
                prompt=prompt,
                n=1,
                size="512x512"
            )

            image_url = response.data[0].url

            # 이미지 URL로부터 이미지 데이터 다운로드
            import requests
            img_data = requests.get(image_url).content

            # media/uploads/llm_images/ 경로에 저장
            save_dir = os.path.join(settings.MEDIA_ROOT, "uploads/llm_images")
            os.makedirs(save_dir, exist_ok=True)
            filename = f"{uuid4().hex}.png"
            file_path = os.path.join(save_dir, filename)
            with open(file_path, "wb") as f:
                f.write(img_data)

            # LLM 객체에 이미지 경로 저장
            llm = LLM.objects.get(id=llm_id)
            llm.llm_image = f"uploads/llm_images/{filename}"
            llm.save()

            return JsonResponse({"image_url": llm.llm_image.url})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)


openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp', 'gif']
MAX_IMAGE_SIZE_MB = 5
ALLOWED_MODELS = ['gpt-4-vision-preview']

def is_allowed_image_file(filename):
    return filename.split('.')[-1].lower() in ALLOWED_IMAGE_EXTENSIONS

@csrf_exempt
def vision_process(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image file provided'}, status=400)

    image_file = request.FILES['image']

    if not is_allowed_image_file(image_file.name):
        return JsonResponse({'error': '지원되지 않는 이미지 형식입니다.'}, status=400)

    if not image_file.content_type.startswith("image/"):
        return JsonResponse({'error': '유효한 이미지 파일이 아닙니다.'}, status=400)

    if image_file.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        return JsonResponse({'error': '이미지 파일이 너무 큽니다. (최대 5MB)'}, status=400)

    try:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print("🔥 Vision Read Error:")
        print(traceback.format_exc())
        return JsonResponse({'error': '이미지를 읽는 중 오류 발생'}, status=500)

    custom_model = request.session.get('custom_model', 'gpt-4o-mini')
    if custom_model not in ALLOWED_MODELS:
        custom_model = 'gpt-4o-mini'

    custom_prompt = request.session.get('custom_prompt', '이 이미지에서 보이는 것을 설명해 주세요.')

    try:
        response = openai_client.chat.completions.create(
            model=custom_model,
            messages=[
                {"role": "system", "content": "You are an assistant that describes images in detail."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": custom_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                    ]
                }
            ]
        )
        ai_result = response.choices[0].message.content.strip()
        time.sleep(3)
        return JsonResponse({"result": ai_result})
    except Exception as e:
        print("🔥 Vision OpenAI Error:")
        print(traceback.format_exc())
        return JsonResponse({"error": f"OpenAI Vision API error: {str(e)}"}, status=500)