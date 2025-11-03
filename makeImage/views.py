import os
import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI, BadRequestError
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from pathlib import Path
from payment.models import TokenHistory, Token
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def make_image_page(request):
    return render(request, "makeImage/image.html")


@csrf_exempt
@login_required
def generate_image(request):
    if request.method != "POST":
        return JsonResponse({"error": _("잘못된 요청입니다.")}, status=400)

    user_input = request.POST.get("prompt")
    if not user_input:
        return JsonResponse({"error": _("프롬프트가 제공되지 않았습니다.")}, status=400)

    # OpenAI 이미지 생성 호출
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=user_input,
            n=1,
            size="1024x1024",
            quality="hd"
        )
    except BadRequestError as e:
        if e.code == "content_policy_violation":
            return JsonResponse({
                "error": _("입력한 프롬프트가 정책에 위배되어 이미지 생성을 할 수 없습니다.")
            }, status=400)
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": _("이미지 생성 중 서버 오류가 발생했습니다.")}, status=500)

    # 토큰 소모 처리
    
    def consume_tokens(user, amount):
        try:
            token_obj = Token.objects.filter(user=user).latest("created_at")
        except Token.DoesNotExist:
            return False

        available_tokens = token_obj.total_token - token_obj.token_usage

        if available_tokens < amount:
            return False

        TokenHistory.objects.create(
            user=user,
            change_type=TokenHistory.CONSUME,
            amount=amount,
            total_voice_generated=amount
        )

        token_obj.token_usage += amount
        token_obj.save()
        return True

    # 이미지 1장당 10토큰 소모 예시
    success = consume_tokens(request.user, 10)
    if not success:
        return JsonResponse({"error": _("보유한 토큰이 부족합니다.")}, status=403)

    # 이미지 URL 반환
    if not response.data or not hasattr(response.data[0], "url"):
        return JsonResponse({"error": _("이미지 생성에 실패했습니다.")}, status=400)

    image_url = response.data[0].url
    return JsonResponse({"image_url": image_url})


@login_required
def proxy_image(request):
    image_url = request.GET.get("url")
    if not image_url:
        return HttpResponse(_("URL이 제공되지 않았습니다."), status=400)
    
    resp = requests.get(image_url)
    if resp.status_code != 200:
        return HttpResponse(_("이미지를 가져오는데 실패했습니다."), status=400)
    
    content_type = resp.headers.get('Content-Type', 'image/png')
    return HttpResponse(resp.content, content_type=content_type)



#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# 앱 전용
def image_app(request):
    return render(request, "makeImage/app/image_app.html")
