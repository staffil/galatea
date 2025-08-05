import os
import base64
from django.shortcuts import render
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
