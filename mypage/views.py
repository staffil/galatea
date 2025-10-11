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
                voice = VoiceList.objects.filter(voice_id=voice_id).first()
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

        if len(prompt) > 700:
            return JsonResponse({"error": _("현재 프롬프트 값이 700자가 넘었습니다.")}, status=400)

        llm.update_at = timezone.now()
        llm.save()

        return JsonResponse({
            "success": True, 
            "message": "AI 설정이 수정되었습니다.",
            "redirect_url": f"/mypage/my_ai_models/{llm.id}/"  # 필요시
        })

    voice_list = VoiceList.objects.filter(user=request.user).order_by('-created_at')
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
@csrf_exempt
def request_refund(request, payment_id):
    """환불 요청 처리"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reason = data.get('reason', '')
            
            # 결제 정보 조회
            payment = Payment.objects.get(id=payment_id, user=request.user)
            
            # 이미 환불된 결제인지 확인
            if payment.status in ['refunded', 'cancelled']:
                return JsonResponse({'error': '이미 환불된 결제입니다.'}, status=400)
            
            # 결제 성공 상태가 아니면 환불 불가
            if payment.status != 'success':
                return JsonResponse({'error': '환불할 수 없는 결제 상태입니다.'}, status=400)
            
            # 토큰 확인
            token = Token.objects.filter(user=request.user).first()
            if not token:
                return JsonResponse({'error': '토큰 정보를 찾을 수 없습니다.'}, status=400)
            
            refund_token_amount = payment.payment_rank.freetoken
            
            # 남은 토큰이 환불할 토큰보다 적은지 확인
            if token.remaining_tokens() < refund_token_amount:
                return JsonResponse({
                    'error': f'토큰을 이미 사용하여 환불할 수 없습니다. (필요: {refund_token_amount}T, 남은: {token.remaining_tokens()}T)'
                }, status=400)
            
            # 환불 사유 저장
            payment.refund_reason = reason
            payment.save()
            
            # PG사에 환불 요청
            result = process_refund(payment)
            
            if result['success']:
                return JsonResponse({
                    'success': True,
                    'message': '환불이 완료되었습니다.',
                    'refunded_amount': float(payment.amount),
                    'refunded_token': refund_token_amount
                })
            else:
                return JsonResponse({
                    'error': result['message']
                }, status=400)
                
        except Payment.DoesNotExist:
            return JsonResponse({'error': '결제 내역을 찾을 수 없습니다.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_access_token():
    """아임포트 Access Token 발급"""
    url = "https://api.iamport.kr/users/getToken"
    data = {
        "imp_key": settings.IAMPORT_API_KEY,
        "imp_secret": settings.IAMPORT_API_SECRET
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"토큰 발급 실패: {response.text}")
    return response.json()["response"]["access_token"]


def process_refund(payment):
    """실제 PG사 환불 처리"""
    try:
        # 아임포트 Access Token 발급
        access_token = get_access_token()
        
        # 환불 API 호출
        url = "https://api.iamport.kr/payments/cancel"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "imp_uid": payment.imp_uid,
            "merchant_uid": payment.merchant_uid,
            "amount": float(payment.amount),
            "reason": payment.refund_reason or "고객 요청 환불",
            "checksum": float(payment.amount)  # 환불 가능 금액 검증
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        print(f"=== 환불 API 응답 ===")
        print(result)
        
        if result['code'] == 0:
            # 환불 성공
            payment.status = 'cancelled'
            payment.refunded_at = timezone.now()
            payment.save()
            
            # 토큰 차감
            token = Token.objects.get(user=payment.user)
            refund_token_amount = payment.payment_rank.freetoken
            token.total_token -= refund_token_amount
            token.save()
            
            # 토큰 히스토리 기록
            TokenHistory.objects.create(
                user=payment.user,
                change_type=TokenHistory.REFUND,  # 모델에 REFUND 추가 필요
                amount=-refund_token_amount,
                total_voice_generated=0
            )
            
            # PaymentStats 업데이트
            stats, _ = PaymentStats.objects.get_or_create(id=1)
            stats.refunded_count += 1
            stats.save()
            
            return {
                'success': True,
                'message': '환불이 완료되었습니다.'
            }
        else:
            # 환불 실패
            return {
                'success': False,
                'message': f"환불 실패: {result.get('message', '알 수 없는 오류')}"
            }
            
    except Exception as e:
        print(f"=== 환불 처리 오류 ===")
        print(str(e))
        return {
            'success': False,
            'message': f'환불 처리 중 오류가 발생했습니다: {str(e)}'
        }

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

@login_required
def token_less(request):
    consume = TokenHistory.objects.filter(
        user=request.user,
        change_type=TokenHistory.CONSUME
    ).order_by("-created_at")

    # ✅ 페이지네이션 추가 (페이지당 10개씩)
    paginator = Paginator(consume, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "mypage/token_less.html", {
        "consume_history": page_obj,  # page_obj 넘김
    })