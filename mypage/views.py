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
from django.utils.translation import gettext_lazy as _

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
            messages.error(request, _("비밀번호가 일치하지 않습니다."))
            return redirect('mypage:mypage_update')

        user.email = email
        user.phonenumber = phonenumber
        user.nickname = nickname
        if user_image:
            user.user_image = user_image
        if password1:
            user.password = make_password(password1)

        user.save()
        messages.success(request, _("프로필이 성공적으로 수정되었습니다."))
        return redirect('mypage:mypage')

    context = {
        'user': user
    }
    return render(request, 'mypage/mypageUpdate.html', context)



@login_required
def my_voice(request):
    user = request.user

    voice_list = VoiceList.objects.filter(user=request.user).select_related("celebrity").order_by("-created_at")
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
def my_voice_delete(request, voice_id):

    if request.method == 'POST':
        user = request.user
        try:
            voice = VoiceList.objects.get(id=voice_id, user=user)
            voice.delete()
            messages.success(request, _("보이스가 삭제되었습니다."))
        except VoiceList.DoesNotExist:
            messages.error(request, _("해당 보이스가 없습니다."))
        
        return redirect('mypage:my_voice')
            

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

# @login_required
# def toggle_voice_public(request, voice_id):
#     voice = get_object_or_404(VoiceList, id=voice_id, user=request.user)

#     voice.is_public = not voice.is_public
#     voice.save()
#     return redirect(request.META.get('HTTP_REFERER', 'mypage:my_voice'))


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
                voice = VoiceList.objects.filter(voice_id=voice_id).order_by("-created_at")
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

        messages.success(request, _('AI 설정이 수정되었습니다.'))
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
        messages.success(request, _("AI가 삭제되었습니다."))
    except LLM.DoesNotExist:
        messages.error(request, _("해당 AI가 없습니다."))

    return redirect("mypage:mypage")



@login_required
@require_POST
def upload_profile_image(request):
    user = request.user
    image_file = request.FILES.get("profile_image")

    if image_file:
        user.profile_image = image_file
        user.save()
        messages.success(request, _("프로필 이미지가 업데이트되었습니다."))
    else:
        messages.error(request, _("이미지 파일을 선택해주세요."))

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




from customer_ai.models import Conversation, Prompt
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


from register.models import Follow
from customer_ai.models import LlmLike
@login_required
def personal_profile(request):
    user = request.user
    llm_list = LLM.objects.filter(user= user, is_public=True)
    prompt_list = Prompt.objects.filter(user= user)
    voice_list = VoiceList.objects.filter(user=user, is_public=True)
    llm = LLM.objects.filter(user=request.user).first()

    llm_paginator = Paginator(llm_list, 3)
    llm_page_number = request.GET.get('llm_page')
    llm_page_obj = llm_paginator.get_page(llm_page_number)

    voice_paginator = Paginator(voice_list, 3)
    voice_page_number = request.GET.get('voice_page')
    voice_page_obj = voice_paginator.get_page(voice_page_number)

    prompt_paginator = Paginator(prompt_list, 3)
    prompt_page_number = request.GET.get('prompt_page')
    prompt_page_obj = prompt_paginator.get_page(prompt_page_number)

    context ={
        "llm_list": llm_page_obj,
        "prompt_list": prompt_page_obj,
        "voice_list": voice_page_obj,
        "llm":llm,
  
    }
    return render(request, "mypage/personal_profile.html", context)



from register.models import Follow
from customer_ai.models import LlmLike
from mypage.models import Genre
from django.utils.translation import get_language
from django.conf import settings
@login_required
def llm_like(request):
    user = request.user
    liked_llms = (
        LlmLike.objects.filter(user=user, is_like=True)
        .select_related("llm")
        .prefetch_related("llm__genres")
    )
    llms = [rel.llm for rel in liked_llms]  

    language = get_language()
    for l in llms:  # 좋아요한 LLM만 돌면 됨
        for g in l.genres.all():
            name_field = f"name_{language}"
            g.display_name = getattr(g, name_field, g.name)

    llm = LLM.objects.filter(user=user).first()


    context = {
        "liked_list": llms,
        "languages": settings.LANGUAGES,
        "llm":llm
    }
    return render(request, "mypage/llm_like.html", context)

# views.py
from django.shortcuts import render, get_object_or_404
from .models import LLM

def llm_intro(request, llm_id):
    llm = get_object_or_404(LLM, id=llm_id)
    return render(request, "llm/intro_partial.html", {"llm": llm})



@login_required
def follow_list(request):
    user = request.user
    following_list = Follow.objects.filter(follower=user).select_related("following")

    follower_list = Follow.objects.filter(following=user).select_related("follower")

    following_ids = set(user.following_set.values_list('following_id', flat=True))
    follower_ids = set(user.follower_set.values_list('follower_id', flat=True))  

    llm = LLM.objects.filter(user=user).first()


    context = {
        "following_list":following_list,
        "follower_list":follower_list,
        "following_ids":following_ids,
        "follower_ids":follower_ids,
        "llm":llm

    }
    return render(request, "mypage/follow_list.html", context)


@login_required
def unpublish_llm(request, llm_id):
    llm = get_object_or_404(LLM, id=llm_id, user=request.user)
    llm.is_public = False
    llm.save()
    return redirect('mypage:personal_profile', llm.id)


@login_required
def prompt_share_delete(request, prompt_id):
    prompt = get_object_or_404(Prompt ,id=prompt_id)

    if request.user != prompt.user:
        messages.error(request, _("삭제 권한이 없습니다."))
        return redirect("mypage/personal_profile.html")
    prompt.delete()
    messages.success(request, _("프롬프트가 삭제되었습니다."))
    return redirect("mypage/personal_profile.html")



from helpdesk.forms import Prompt,PromptForm
@login_required
def prompt_share_update(request, prompt_id):
    prompt = get_object_or_404(Prompt, id= prompt_id)

    if request.user != prompt.user:
        messages.error(request, _("수정 권한이 없습니다."))
        return redirect("mypage/personal_profile.html")
    
    if request.method =="POST":
        form = PromptForm(request.POST , instance=prompt)
        if form.is_valid():
            form.save()
            messages.success(request, _("프롬프트가 수정되었습니다."))
            return redirect("mypage/personal_profile.html")
        
    else:
        form = PromptForm(instance=prompt)

    return render(request, "mypage/personal_profile.html")




import secrets
import string
from django.contrib.auth.decorators import login_required

def generate_code(length=10):
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


import secrets, string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from user_auth.models import Referral, Coupon
from .models import LLM  # 필요시 import

# 랜덤 코드 생성
def generate_code(length=12):
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

@login_required
def my_coupon(request):
    user = request.user
    llm = LLM.objects.filter(user=user).first()

    if request.method == "POST":
        input_code = request.POST.get("invite_code", "").strip()

        try:
            referral = Referral.objects.get(code=input_code, is_active=True)
        except Referral.DoesNotExist:
            messages.error(request, "유효하지 않거나 이미 사용된 코드입니다.")
            return redirect("mypage:my_coupon")

        if Referral.objects.filter(invitee=user).exists():
            messages.error(request, "이미 다른 초대 코드를 사용했습니다.")
            return redirect("mypage:my_coupon")

        # Referral 업데이트
        referral.invitee = user
        referral.is_active = False
        referral.save()

        # 1️⃣ 초대받은 사람(B)에게 토큰 충전
        token_b, _ = Token.objects.get_or_create(user=user)
        token_b.total_token += 0  # 충전량
        token_b.save()

        TokenHistory.objects.create(
            user=user,
            change_type=TokenHistory.CHARGE,
            amount=100
        )

        # 2️⃣ 초대한 사람(A)에게 토큰 충전
        token_a, _ = Token.objects.get_or_create(user=referral.inviter)
        token_a.total_token += 100
        token_a.save()


        messages.success(request, "초대 코드가 적용되었습니다! 토큰이 지급되었습니다.")
        return redirect("mypage:my_coupon")

    # GET 요청: 토큰 내역 보여주기
    user_tokens = TokenHistory.objects.filter(user=user).order_by('-created_at')
    context = {
        "user_tokens": user_tokens,
        "token_obj": Token.objects.filter(user=user).first(),
        "llm":llm

    }
    return render(request, "mypage/my_coupon.html", context)
