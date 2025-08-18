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
from django.utils.safestring import mark_safe
import json
from django.db.models.functions import TruncDate

@login_required
def personal_token(request):
    user = request.user

    # GET 파라미터로 날짜 범위 받기, 없으면 최근 20일
    end_date_str = request.GET.get('end_date')
    start_date_str = request.GET.get('start_date')

    today = timezone.localdate()

    # 날짜 파싱
    try:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else today
    except ValueError:
        end_date = today

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else end_date - timedelta(days=20)
    except ValueError:
        start_date = end_date - timedelta(days=20)

    # timezone-aware datetime
    start_datetime = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
    end_datetime = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))

    # 일별 토큰 사용량 집계 (consume)
    token_daily_qs = (
        TokenHistory.objects
        .filter(
            user=user,
            change_type=TokenHistory.CONSUME,
            created_at__gte=start_datetime,
            created_at__lte=end_datetime
        )
        .annotate(day=TruncDate('created_at', tzinfo=timezone.get_current_timezone()))
        .values('day')
        .annotate(daily_usage=Sum('amount'))
        .order_by('day')
    )

    # 날짜별 사용량 dict
    usage_dict = {t['day'].strftime("%Y-%m-%d"): t['daily_usage'] for t in token_daily_qs if t['day']}

    # 전체 날짜 범위 채우기 (0 포함)
    labels = []
    data = []
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        labels.append(date_str)
        data.append(usage_dict.get(date_str, 0))
        current_date += timedelta(days=1)

    # 결제 정보
    payments = Payment.objects.all()

    context = {
        'labels': labels,
        'data': data,
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d"),
        'payments': payments,
    }

    return render(request, 'mypage/token.html', context)


@login_required
def my_custom(request):
    return render(request, "mypage/my_custom.html")


@login_required
def my_request(request):
    if request.user:
        request_list = Requests.objects.filter(user=request.user)

        context = {
            "request_list": request_list
        }

        
    return render(request, "mypage/my_request.html", context)


@login_required
def my_coupon(request):
    return render(request, "mypage/my_coupon.html")