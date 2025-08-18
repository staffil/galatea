from django.shortcuts import render, redirect, get_object_or_404
from mypage.models import  Genre
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import base64
from makeVoice.models import VoiceList, VoiceLike
from customer_ai.models import LLM, LlmLike
from register.models import Follow
from django.utils.translation import get_language
from home.models import Users

@csrf_exempt
@login_required
def distribute(request, llm_id):
    llm = get_object_or_404(LLM, id=llm_id)
    genre_list = Genre.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        distribute_text = request.POST.get('distribute')
        selected_genres = request.POST.getlist('genre')
        llm_background_img = request.FILES.get('background_image')

        if not distribute_text or not title:
            return JsonResponse({"error": "해당 AI 설명을 해주세요"})
        if not llm_background_img:
            return JsonResponse({"error": "배경사진을 추가해 주세요"})
        llm.title = title
        llm.description = distribute_text
        llm.is_public = True

        # 장르 ManyToMany 필드 업데이트
        llm.genres.set(selected_genres)

        if llm_background_img:
            llm.llm_background_image = llm_background_img

        llm.save()

        return redirect("home:main")

    else:
        # GET 요청 시 기존 선택된 장르 id 문자열 리스트로
        selected_genres = list(map(str, llm.genres.values_list('id', flat=True)))

    context = {
        "llm": llm,
        "genre_list": genre_list,
        "selected_genres": selected_genres,
    }
    return render(request, "distribute/distribute.html", context)



@login_required
def unpublish_llm(request, llm_id):
    llm = get_object_or_404(LLM, id=llm_id, user=request.user)
    llm.is_public = False
    llm.save()
    return redirect('mypage:my_ai_models', llm.id)


