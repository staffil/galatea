from django.shortcuts import render ,redirect,get_object_or_404
from home.models import Users
from django.contrib.auth.decorators import login_required
from user_auth.models import LLM, Voice
from django.core.files.storage import default_storage
from django.utils import timezone
import os
from makeVoice.models import VoiceList
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

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
    paginator = Paginator(voice_list, 10) 
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
                voice = Voice.objects.get(voice_id=voice_id)
            except Voice.DoesNotExist:
                voice = Voice.objects.create(user=request.user, voice_id=voice_id)
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
    paginator = Paginator(voice_list, 10)
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