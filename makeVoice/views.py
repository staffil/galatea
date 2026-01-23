import os
import base64
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from openai import OpenAI
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
from makeVoice.models import VoiceList
from django.contrib.auth.decorators import login_required

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
eleven_client = ElevenLabs(api_key=ELEVEN_API_KEY)

@login_required 
@require_http_methods(["GET"])
def make_voice_page(request):
    return render(request, "makeVoice/makeVoice.html", {
        "is_result": False,
        "voice_prompt_input": request.session.get('voice_prompt', ''),
        "sample_text_input": request.session.get('sample_text', ''),
        "voice_name": request.session.get("voice_name", '')
    })


def is_voice_error(prompt, text):
    if not prompt or not text:
        return "프롬프트와 샘플 텍스트를 입력하세요"
    elif len(prompt) < 20:
        return "프롬프트는 20자 이상이어야 합니다."
    elif len(prompt) > 500:
        return "프롬프트는 500자를 넘으면 안됩니다."
    elif len(text) < 100:
        return "샘플 텍스트는 100자 이상이어야 합니다."
    return None 

from payment.models import Token
from payment.models import TokenHistory
from pydub import AudioSegment

def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    return int(audio.duration_seconds)

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
@login_required 
@require_http_methods(["POST"])
def sample_voice(request):
    voice_prompt = request.POST.get('voice_prompt_input', '').strip()
    sample_text = request.POST.get('sample_text_input', '').strip()

    error_msg = is_voice_error(voice_prompt, sample_text)
    if error_msg:
        return render(request, "makeVoice/makeVoice.html", {
            "is_result": False,
            "error": error_msg,
            "voice_prompt_input": voice_prompt,
            "sample_text_input": sample_text
        })
    try:
        design_response = eleven_client.text_to_voice.design(
            model_id="eleven_multilingual_ttv_v2",
            voice_description=voice_prompt,
            text=sample_text,
            
        )
    
        if design_response and design_response.previews:
            preview = design_response.previews[0]
            gen_id = preview.generated_voice_id
            audio_data = base64.b64decode(preview.audio_base_64)

            file_name = default_storage.save(f"audio_previews/{gen_id}.mp3", ContentFile(audio_data))
            file_url = default_storage.url(file_name)
            file_path = default_storage.path(file_name)
            audio_second = get_audio_duration(file_path)


            def consume_token(user, amount):
                with transaction.atomic():
                    try:
                        token_obj = Token.objects.select_for_update().get(user=user)
                    except ObjectDoesNotExist:
                        return False 

                    avail_token = token_obj.total_token - token_obj.token_usage
                    if avail_token < amount:
                        return False

                    token_obj.token_usage += amount
                    token_obj.save()

                    TokenHistory.objects.create(
                        user=user,
                        change_type=TokenHistory.CONSUME,
                        amount=amount,
                        total_voice_generated=amount
                    )
                    return True
            
            success = consume_token(request.user, audio_second)
            if not success:
                return JsonResponse({"error": "토큰이 부족합니다."}, status = 403)


            request.session['voice_prompt'] = voice_prompt
            request.session['sample_text'] = sample_text
            request.session['preview_id'] = gen_id
            request.session['preview_url'] = file_url

            request.session['sample_url'] = file_url
            request.session['generated_voice_id'] = gen_id

       
            return render(request, "makeVoice/makeVoice.html", {
                "is_result": True,
                "preview_id": gen_id,
                "preview_url": file_url,
                "voice_prompt_input": voice_prompt,
                "sample_text_input": sample_text
            })
        else:
            return render(request, "makeVoice/makeVoice.html", {
                "is_result": False,
                "error": "샘플을 생성할 수 없습니다.",
                "voice_prompt_input": voice_prompt,
                "sample_text_input": sample_text
            })
    except Exception as e:
        error_str = str(e)
        if "blocked_generation" in error_str or "Sorry, this prompt potentially doesn't follow our safety guidelines" in error_str:
            user_error_msg = "프롬프트에 부적절한 내용이 있습니다. 폭력, 성적인 단어, 아이, 어린애 단어는 넣지 마십시오."
        else:
            user_error_msg = f"오류 발생: {error_str}"
        return render(request, "makeVoice/makeVoice.html", {
            "is_result": False,
            "error": user_error_msg,
            "voice_prompt_input": voice_prompt,
            "sample_text_input": sample_text
        })

@csrf_exempt
@login_required 
@require_http_methods(["GET", "POST"])
def make_voice(request):
    if request.method == "GET":
        return render(request, 'makeVoice/makeVoice.html')
    
    elif request.method == "POST":
        generated_voice_id = request.POST.get("generated_voice_id")
        voice_name = request.POST.get("voice_name", "").strip()
        voice_description = request.session.get('voice_prompt', '').strip()
        sample_url = request.session.get("sample_url")

        voice_description = voice_description[:500]
        

        # 유효성 검사
        if not generated_voice_id:
            return JsonResponse({"status": "error", "error": "generated_voice_id가 없습니다."})
        if len(voice_description) > 500:
            return JsonResponse({"status": "error", "error": "voice_description은 500자 이하로 입력하세요."})
        if not voice_name:
            return JsonResponse({"status": "error", "error": "voice_name을 입력하세요."})
        if not sample_url:
            return JsonResponse({"status": "error", "error": "sample_url이 없습니다. 먼저 샘플을 생성하세요."})

        try:
            # 실제 생성
            create_response = eleven_client.text_to_voice.create(
                generated_voice_id=generated_voice_id,
                voice_name=voice_name,
                voice_description=voice_description,
            )

            print(f"[DEBUG] Saving voice_id: {create_response.voice_id}, sample_url: {sample_url}")
            voice = VoiceList.objects.create(
                user=request.user,
                voice_id=create_response.voice_id,
                voice_name=voice_name,
                sample_url=sample_url
            )
            voice.save()

            request.session['final_voice_id'] = create_response.voice_id

            return JsonResponse({"status": "success", "voice_id": create_response.voice_id})

        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)})
import openai
import json
@csrf_exempt
def auto_generate_prompt(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_prompt = data.get("prompt", "").strip()

            if not user_prompt:
                return JsonResponse({"status": "error", "error": "프롬프트가 비어있습니다."})

            # OpenAI API 호출 (1.0+ 방식)
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 음성 프롬프트를 전문적으로 개선하는 AI입니다. 다른 말은 넣지 말고 사용자가 적은 프롬프트를 elevenlabs 프롬프트 형식으로 만들고 영어로 만들어주세요. 그리고 프롬프트를 100자 넘게 만들어 주세요"},
                    {"role": "user", "content": user_prompt}
                ]
            )

            # ✅ 1.0+ 접근 방식
            refined_prompt = response.choices[0].message.content

            return JsonResponse({"status": "success", "refined_prompt": refined_prompt})

        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)})

    return JsonResponse({"status": "error", "error": "POST 요청만 허용됩니다."})


import requests
from django.utils import timezone
from makeVoice.models import VoiceList
from celebrity.models import CelebrityVoice
# sync 일레븐 랩스
def sync_voices_with_type():
    """
    ElevenLabs의 모든 보이스를 DB에 동기화
    (user=None으로 저장하여 시스템 보이스로 관리)
    """
    ELEVEN_API_KEY = os.getenv('ELEVEN_API_KEY')
    eleven_client = ElevenLabs(api_key=ELEVEN_API_KEY)

    try:
        print("ElevenLabs 클라이언트 초기화 완료:", eleven_client)

        # 모든 보이스 가져오기
        all_voices = eleven_client.voices.get_all().voices
        print(f"총 {len(all_voices)}개 보이스 가져옴")

        for v in all_voices:
            celebrity_voice_id = getattr(v, "voice_id", None)
            if not celebrity_voice_id:
                print(f"⚠️ voice_id 없음, 스킵: {getattr(v, 'name', 'unknown')}")
                continue


            # DB에 저장 (user=None으로 시스템 보이스)
            voice, created = CelebrityVoice.objects.update_or_create(
                celebrity_voice_id=celebrity_voice_id,
                defaults={
                    "name": getattr(v, "name", "Unknown"),
                    "created_at": timezone.now(),
                }
            )
            # preview_url 가져오기
            preview_url = getattr(v, "preview_url", None)
            if preview_url:
                try:
                    r = requests.get(preview_url, timeout=10)
                    if r.status_code == 200:
                        filename = f"{voice.name}_{voice.celebrity_voice_id}.mp3".replace(" ", "_")
                        voice.sample_url.save(filename, ContentFile(r.content), save=True)
                except Exception as e:
                    print(f"⚠️ 샘플 오디오 다운로드 실패: {voice.name}, {e}")

            print(f"{'생성' if created else '업데이트'}: {voice.name}")

        print("✅ Voice sync 저장 완료")

    except Exception as e:
        print("❌ Voice sync 실패:", e)

