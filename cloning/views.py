import os
import base64
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from makeVoice.models import VoiceList
from cloning.models import CloningAgreement

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
eleven_client = ElevenLabs(api_key=ELEVEN_API_KEY)



@login_required
@require_http_methods(["GET"])
def voice_cloning_page (request):
    cloning_agreement = CloningAgreement.objects.all()
    context = {
        "cloning_agreement": cloning_agreement
    }
    return render(request, "cloning/cloning.html", context)



from payment.models import Token
from payment.models import TokenHistory
from pydub import AudioSegment

def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    return int(audio.duration_seconds)

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import json
@login_required
@csrf_exempt
def save_consent(request):
    if request.method != "POST":
        return JsonResponse({"status":"error","error":"POST 요청만 허용됩니다."}, status=405)

    data = json.loads(request.body)
    consent_voice = data.get("consent_voice", False)
    consent_third = data.get("consent_third", False)
    consent_share = data.get("consent_share", False)

    # update_or_create로 체크박스만 저장
    agreement, created = CloningAgreement.objects.update_or_create(
        user=request.user,
        defaults={
            "consent_voice": consent_voice,
            "consent_third": consent_third,
            "consent_share": consent_share
        }
    )
    return JsonResponse({"status":"success"})

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def voice_cloning_sample(request):

    try:
        agreement = CloningAgreement.objects.get(user =request.user)
        if not (agreement.consent_voice and agreement.consent_share and agreement.consent_share):
            return JsonResponse({"status":"error", "error":"음성 클로닝을 사용하려면 동의서에 동의 하셔야 합니다."}, status=403)
        

    except CloningAgreement.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "error": "동의서가 존재하지 않습니다. 먼저 동의서를 확인해주세요."
        }, status=403)

    
    audio_file = request.FILES.get('audio')
    voice_name = request.POST.get('voice_name', '').strip()
    sample_text = request.POST.get('sample_text', '').strip()
    from inspect import signature
    sig = signature(eleven_client.voices.ivc.create)
    print(sig)
    if not audio_file:
        return JsonResponse({"status":"error", "error": "오디오 파일이 비었습니다."})
    if not voice_name:
        return JsonResponse({"status":"error", "error": "voice 이름을 적지 않았습니다."})
    if not sample_text:
        return JsonResponse({"status": "error", "error": "샘플 텍스트를 적어주세요"})
    

    try:
        cloning_audio = default_storage.save(f"cloning_audio/{audio_file.name}", ContentFile(audio_file.read()))

        full_audio_path = default_storage.path(cloning_audio)

        with open(full_audio_path, 'rb') as f:
            voice_clone_resp = eleven_client.voices.ivc.create(
                name = voice_name,
                files = [("audio_file", f)],
            )

        audio_second = get_audio_duration(full_audio_path)
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

        

        voice_id = voice_clone_resp.voice_id

        tts_response = eleven_client.text_to_voice.generate(
            voice_id = voice_id,
            text= sample_text
        )
        audio_byte = tts_response.read()

        file_name = f"cloning_samples/{voice_id}_sample.mp3"
        saved_path = default_storage.save(file_name, ContentFile(audio_byte))
        sample_url = default_storage.url(saved_path)

        default_storage.delete(cloning_audio)

        return JsonResponse({
            "status": "success",
            "voice_id": voice_id,
            "sample_url": sample_url
        })
    
    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)})
    

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def voice_cloning_save(request):
    import json
    data = json.loads(request.body)
    voice_id = data.get("voice_id")
    voice_name = data.get("voice_name", "").strip()

    if not voice_id or not voice_name:
        return JsonResponse({"status": "error", "error": "voice_id와 voice_name을 모두 입력하세요."})

    try:
        if VoiceList.objects.filter(voice_id=voice_id, user=request.user).exists():
            return JsonResponse({"status": "error", "error": "이미 저장된 목소리입니다."})

        voice = VoiceList.objects.create(
            user = request.user,
            voice_id= voice_id,
            voice_name = voice_name,
            sample_url=f"/media/cloning_samples/{voice_id}_sample.mp3"
            
            )

        voice.save()

        return JsonResponse({"status": "success"})
    
    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)})


    
