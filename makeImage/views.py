import os
import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
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
    if request.method == "POST":
        user_input = request.POST.get("prompt")
        if not user_input:
            return JsonResponse({"error": _("프롬프트가 제공되지 않았습니다.")}, status=400)

        response = client.images.generate(
            model="dall-e-3",
            prompt=user_input,
            n=1,
            size="1024x1024",
            quality="hd"
        )
        def consume_tokens(user, amount):
            # 모델별 배율
            required_tokens = amount

            token_obj = Token.objects.filter(user=user).latest("created_at")
            available_tokens = token_obj.total_token - (token_obj.token_usage * 10)

            if available_tokens < required_tokens:
                return False



            TokenHistory.objects.create(
                user=user,
                change_type=TokenHistory.CONSUME,
                amount=required_tokens,
                total_voice_generated=required_tokens
            )
            return True


        success = consume_tokens(request.user, response)
        if not success:
            return JsonResponse({"error": _("보유한 토큰이 부족합니다.")}, status=403)

        image_url = response.data[0].url
        return JsonResponse({"image_url": image_url})

    return JsonResponse({"error": _("잘못된 요청입니다.")}, status=400)


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