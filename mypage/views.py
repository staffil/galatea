from django.shortcuts import render ,redirect,get_object_or_404
from home.models import Users
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.utils import timezone
import os
from mypage.models import LLM
from makeVoice.models import VoiceList
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from payment.models import Payment, PaymentMethod, PaymentRank, PaymentStats,Token, TokenHistory, TotalToken
from user_auth.models import Requests

# Create your views here.
@login_required(login_url='/register/login/')
def mypage_view(request):
    user = request.user  
    llm = LLM.objects.filter(user=user).first()
    context = {
        'user': user,
        "llm":llm
    }
    return render(request, "mypage/mypage.html", context)
@login_required

@login_required
def mypage_update(request):
    user = request.user

    if request.method == 'POST':
        nickname = request.POST.get("nickname")
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_image = request.FILES.get('user_image')

        if password1 != password2:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            return redirect('mypage:mypage_update')

        user.email = email
        user.phonenumber = phonenumber
        user.nickname = nickname
        if user_image:
            user.user_image = user_image
        if password1:
            user.password = make_password(password1)

        user.save()
        messages.success(request, "프로필이 성공적으로 수정되었습니다.")
        return redirect('mypage:mypage')

    context = {
        'user': user
    }
    return render(request, 'mypage/mypageUpdate.html', context)



@login_required
def my_voice(request):
    user = request.user

    voice_list = VoiceList.objects.filter(user=request.user).order_by('created_at')
    paginator = Paginator(voice_list, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    llm = LLM.objects.filter(user=user).first()


    context = {
        'voice_list': page_obj,
        "llm":llm

    }
    return render(request, "mypage/my_voice.html",context)

@login_required
def my_ai_models(request, llm_id):
    user = request.user
    llm_list = LLM.objects.filter(user=user).select_related('voice')
    llm= get_object_or_404(LLM, id=llm_id)
    context = {
        "llm_list" : llm_list,
        "llm":llm
    }
    return render(request, "mypage/my_ai_models.html", context)

@login_required
def toggle_voice_public(request, voice_id):
    voice = get_object_or_404(VoiceList, id=voice_id, user=request.user)

    voice.is_public = not voice.is_public
    voice.save()
    return redirect(request.META.get('HTTP_REFERER', 'mypage:my_voice'))


from django.views.decorators.http import require_POST

from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@csrf_exempt
@login_required
def my_ai_models_update(request, llm_id):
    llm = get_object_or_404(LLM, id=llm_id)

    if request.method == "POST":
        user = request.user

        name = request.POST.get("name", llm.name)
        prompt = request.POST.get("prompt", llm.prompt)
        model = request.POST.get("model", llm.model)
        voice_id = request.POST.get("voice_id", llm.voice.voice_id if llm.voice else None)
        stability = request.POST.get("stability")
        speed = request.POST.get("speed")
        style = request.POST.get("style")
        language = request.POST.get("language", llm.language)
        temperature = request.POST.get("temperature")

        llm.name = name
        llm.prompt = prompt
        llm.model = model

        if voice_id:
            try:
                voice = VoiceList.objects.get(voice_id=voice_id)
            except VoiceList.DoesNotExist:
                voice = VoiceList.objects.create(user=request.user, voice_id=voice_id)
            llm.voice = voice

        if stability not in [None, ""]:
            llm.stability = float(stability)

        if speed not in [None, ""]:
            llm.speed = float(speed)

        if style not in [None, ""]:
            llm.style = float(style)

        if language:
            llm.language = language

        if temperature not in [None, ""]:
            llm.temperature = float(temperature)

        if 'llm_image' in request.FILES:
            llm.llm_image = request.FILES['llm_image']

        llm.update_at = timezone.now()
        llm.save()

        messages.success(request, 'AI 설정이 수정되었습니다.')
        return redirect("mypage:my_ai_models", llm_id=llm.id)

    voice_list = VoiceList.objects.filter(user=request.user).order_by('created_at')
    paginator = Paginator(voice_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'voice_list': page_obj,
        "llm": llm
    }
    return render(request, "mypage/my_ai_modelsUpdate.html", context)


@login_required
def my_ai_models_delete(request, llm_id):
    user = request.user
    try:
        llm = LLM.objects.get(id=llm_id, user=user)
        llm.delete()
    except LLM.DoesNotExist:
        messages.error("해당 AI 가 없습니다.")

    return redirect("mypage:mypage")

@login_required
def my_voice_delete(request, voice_id):

    if request.method == 'POST':
        user = request.user
        try:
            voice = VoiceList.objects.get(id=voice_id, user=user)
            voice.delete()
            messages.success(request, "보이스가 삭제되었습니다.")
        except VoiceList.DoesNotExist:
            messages.error("해당 보이스가 없습니다.")
        
        return redirect('mypage:my_voice')
            

@login_required
@require_POST
def upload_profile_image(request):
    user = request.user
    image_file = request.FILES.get("profile_image")

    if image_file:
        user.profile_image = image_file
        user.save()
        messages.success(request, "프로필 이미지가 업데이트되었습니다.")
    else:
        messages.error(request, "이미지 파일을 선택해주세요.")

    return redirect("mypage:mypage")

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime, timedelta


@login_required
def personal_token(request):
    user = request.user

    # 유저 토큰 정보 가져오기
    token = Token.objects.filter(user=user).first()

    remaining = token.remaining_tokens() if token else 0
    total = token.total_token if token else 0
    used = token.token_usage if token else 0

    # 결제 내역
    payments = Payment.objects.filter(user=user).order_by('-paid_at')

    # LLM 정보
    llm = LLM.objects.filter(user=user).first()

    usage_percent = 0
    if token and token.total_token > 0:
        usage_percent = (token.token_usage / token.total_token) * 100


    context = {
        'remaining': remaining,
        'total': total,
        'used': used,
        'payments': payments,
        'llm': llm,
        'usage_percent': usage_percent,


    }

    return render(request, 'mypage/token.html', context)


@login_required
def my_custom(request):
    return render(request, "mypage/my_custom.html")


@login_required
def my_request(request):
    if request.user:
        request_list = Requests.objects.filter(user=request.user)
        llm = LLM.objects.filter(user=request.user).first()
        

        context = {
            "request_list": request_list,
            "llm": llm
        }

        
    return render(request, "mypage/my_request.html", context)


@login_required
def my_coupon(request):
    llm = LLM.objects.filter(user=request.user).first()
    context={
        "llm":llm
    }

    return render(request, "mypage/my_coupon.html", context)


from customer_ai.models import Conversation
@login_required
def my_ai_conversation(request, llm_id):
    user = request.user
    llm_list = Conversation.objects.filter(user=user)
    llm= get_object_or_404(LLM, id=llm_id)
    context = {
        "llm_list" : llm_list,
        "llm":llm
    }
    return render(request, "mypage/my_ai_conversation.html", context)