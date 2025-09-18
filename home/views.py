from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib.auth import logout, get_user_model
from django.utils.translation import get_language
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime
import random
from user_auth.models import News
from celebrity.models import Celebrity, CelebrityVoice
from mypage.models import Genre
from customer_ai.models import LLM, LlmLike
from makeVoice.models import VoiceList, VoiceLike
from register.models import Follow
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from distribute.models import Comment
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from user_auth.models import Gift
from django.db.models import Count

User = get_user_model()

# 기본 뷰 함수들
def home(request):
    return render(request, 'home/home.html')
def main(request):
    language = get_language()
    user = request.user
    genre_list = Genre.objects.all().order_by("?")
    voice_list = VoiceList.objects.filter(is_public=True)
    celebrity_voice_list = CelebrityVoice.objects.all().order_by("?")
    news_list = News.objects.all()
    total_follow_count = User.objects.annotate(follower_count = Count('follower_set', distinct=True)).order_by("-follower_count")[:10]
    

    # LLM 랜덤 캐시 처리
    now = datetime.now()
    hour_key = now.strftime('%Y%m%d_%H')
    cache_key = f'llm_random_list_{language}_{hour_key}'
    llm_cache_key = f'llm_random_list_{language}_{hour_key}'
    voice_cache_key = f'voice_random_list_{language}_{hour_key}'


    llm_list_ids = cache.get(llm_cache_key)
    if llm_list_ids is None:
        llm_list_ids = list(LLM.objects.filter(is_public=True).values_list('id', flat=True))
        random.shuffle(llm_list_ids)
        cache.set(llm_cache_key, llm_list_ids, timeout=10)

    voice_list_ids = cache.get(voice_cache_key)
    if voice_list_ids is None:
        voice_list_ids = list(VoiceList.objects.filter(is_public=True).values_list('id', flat=True))
        random.shuffle(voice_list_ids)
        cache.set(voice_cache_key, voice_list_ids, timeout=10)


    # 캐시된 순서대로 LLM 객체 가져오기
    llm_list = list(LLM.objects.filter(id__in=llm_list_ids).prefetch_related('genres'))
    llm_list.sort(key=lambda x: llm_list_ids.index(x.id))
    if request.user.is_authenticated:
        for llm in llm_list:
            try:
                like_obj = LlmLike.objects.get(user=request.user, llm=llm, is_like=True)
                llm.user_has_liked = True
            except LlmLike.DoesNotExist:
                llm.user_has_liked = False
    else:
        for llm in llm_list:
            llm.user_has_liked = False
    voice_list = list(VoiceList.objects.filter(id__in = voice_list_ids).prefetch_related('llm'))
    voice_list.sort(key=lambda x: voice_list_ids.index(x.id))

    gift_list = Gift.objects.all()

    # 다국어 이름/설명 처리

    llm_list2 = list(
        LLM.objects.filter(id__in=llm_list_ids)
        .annotate(like_count=Count('llm_like_count', filter=Q(llm_like_count=True)))
        .order_by('-like_count') 
    )



    for l in llm_list:
        l.display_genres = []
        for g in l.genres.all():
            name_field = f'name_{language}'
            g.display_name = getattr(g, name_field, g.name)
            l.display_genres.append(g)

    context = {
        "languages": settings.LANGUAGES,
        "LANGUAGE_CODE": language,
        "request": request,
        "genre_list": genre_list,
        "user": user,
        "llm": llm_list,
        "llm_list": llm_list,
        "llm_list2": llm_list2,
        "voice_list": voice_list,
        "celebrity_voice_list": celebrity_voice_list,
        "news_list": news_list,
        "total_follow_count":total_follow_count,
        "gift_list" : gift_list,
    }

    return render(request, 'home/main.html', context)


def user_logout(request):
    logout(request)
    return redirect('register:login') 

# users 테이블에 데이터 삽입 함수 (함수만 정의, 바로 실행하지 않음)
def insert_users_raw_sql():
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO users (user_name, email, password, nickname, phonenumber) VALUES
            ('user1', 'user1@gmail.com', '1234', 'JohnnyD', '010-1234-5678'),
            ('admin1', 'admin@gmail.com', '1234', 'JaneS', '010-9876-5432')
        """)

# users 테이블에서 데이터 조회 함수
def select_users():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
    return rows

from django.shortcuts import render, get_object_or_404
from customer_ai.models import LLM

def llm_detail_partial(request, llm_id):
    llm = get_object_or_404(LLM, id=llm_id)
    
    # 좋아요 정보 추가!
    if request.user.is_authenticated:
        try:
            like_obj = LlmLike.objects.get(user=request.user, llm=llm, is_like=True)

            llm.user_has_liked = True
        except LlmLike.DoesNotExist:
            llm.user_has_liked = False
    else:
        llm.user_has_liked = False

    if request.user.is_authenticated:
        llm.user_is_following_user = Follow.objects.filter(follower=request.user, following=llm.user).exists()
    else:
        llm.user_is_following_user = False

    
    
    return render(request, 'home/llm_intro.html', {'llm_list': [llm]})


# llm_intro에 들어갈 뷰
def distribute_llm(request, llm_id=None):
    language = get_language()
    user = request.user

    genre_list = Genre.objects.all()
    llm_list = LLM.objects.filter(is_public=True).prefetch_related('genres')

    # 각 LLM에 좋아요 정보 직접 추가
    if request.user.is_authenticated:
        for llm in llm_list:
            try:
                like_obj = LlmLike.objects.get(user=user, llm=llm, is_like=True)
                llm.user_has_liked = True
            except LlmLike.DoesNotExist:
                llm.user_has_liked = False
    else:
        for llm in llm_list:
            llm.user_has_liked = False

    # 장르 이름 처리
    for l in llm_list:
        l.display_genres = []
        for g in l.genres.all():
            name_field = f'name_{language}'
            g.display_name = getattr(g, name_field, g.name)
            l.display_genres.append(g)

    voice_list = VoiceList.objects.filter(is_public=True)

    context = {
        "genre_list": genre_list,
        "user": user,
        "llm_list": llm_list,
        "voice_list": voice_list,
        "LANGUAGE_CODE": language, 
    }

    return render(request, 'home/llm_intro.html', context)

@login_required
def follow_toggle(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': _('요청할 수 없습니다.')}, status=405)

    user_id = request.POST.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': _('user_id가 필요합니다.')}, status=400)

    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': _('존재하지 않는 사용자입니다.')}, status=404)

    follow_relation = Follow.objects.filter(follower=request.user, following=target_user).first()
    if follow_relation:
        # 언팔로우
        follow_relation.delete()
        target_user.follow_count = max(target_user.follow_count - 1, 0)
        target_user.save()
        status = 'unfollow'
    else:
        # 팔로우
        Follow.objects.create(follower=request.user, following=target_user)
        target_user.follow_count += 1
        target_user.save()
        status = 'follow'

    return JsonResponse({'status': status, 'follow_count': target_user.follow_count})



from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from customer_ai.models import LLM, LlmLike

@login_required
def like_toggle(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': _('요청할 수 없습니다.')}, status=405)

    llm_id = request.POST.get("llm_id")
    if not llm_id:
        return JsonResponse({'status': 'error', 'message': _('llm_id가 필요합니다.')}, status=400)

    try:
        target_llm = LLM.objects.get(id=llm_id)
    except LLM.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': _('존재하지 않는 LLM입니다.')}, status=404)

    user = request.user

    # LlmLike 존재 여부 확인 후 생성 또는 업데이트
    llm_like, created = LlmLike.objects.get_or_create(
        user=user, llm=target_llm, defaults={'is_like': True}
    )

    if not created and llm_like.is_like:  # 이미 좋아요면 취소
        llm_like.is_like = False
        target_llm.llm_like_count = max(target_llm.llm_like_count - 1, 0)
        status = 'unlike'
    else:  # 좋아요
        llm_like.is_like = True
        target_llm.llm_like_count += 1
        status = 'like'

    llm_like.save()
    target_llm.save()

    return JsonResponse({'status': status, 'like_count': target_llm.llm_like_count})

# views.py
from django.http import Http404

def llm_intro(request, llm_id):
    # id로 특정 LLM을 가져오면서 is_public=True 조건 적용
    try:
        llm = LLM.objects.get(id=llm_id, is_public=True)
    except LLM.DoesNotExist:
        raise Http404(_("LLM을 찾을 수 없습니다."))
    
    # 팔로우 여부 확인
    is_following = request.user in llm.user.followers.all()
    
    return render(request, 'home/llm_intro.html', {
        'llm_list': [llm],       # 템플릿에서는 for문으로 사용
        'followers_ids': is_following,
    })



def gerne_all(request):
    genre = Genre.objects.all()
    llm_list = LLM.objects.all()
    language = get_language()


    for l in llm_list:
        for g in l.genres.all():
            name_field = f'name_{language}'
            g.display_name = getattr(g, name_field, g.name)
    context = {
        "languages": settings.LANGUAGES,
        "genre_list": genre,

    }

    return render(request,'home/genres.html', context)


#검색하기
def search_llm(request):
    query = request.GET.get('q', '')
    result = []

    if query:
        result = LLM.objects.filter(title__icontains = query, is_public=True)
    return render(request, 'common/search_result.html', {
        'query': query,
        'results': result
    })


def genre_detail(request, genres_id):
    genres = get_object_or_404(Genre, id =genres_id)

    llm_list = genres.llms.all().order_by("?")
    language_code = getattr(request, 'LANGUAGE_CODE', get_language()) or 'ko'

    context ={
        "genres": genres,
        "llm_list": llm_list,
        "LANGUAGE_CODE": language_code
    }
    return render (request, "home/genres_detail.html", context)


def llm_section(request):
    

    language_code = getattr(request, 'LANGUAGE_CODE', get_language()) or 'ko'
    language = get_language()

        # LLM 랜덤 캐시 처리
    now = datetime.now()
    hour_key = now.strftime('%Y%m%d_%H')
    cache_key = f'llm_random_list_{language}_{hour_key}'
    llm_cache_key = f'llm_random_list_{language}_{hour_key}'
    voice_cache_key = f'voice_random_list_{language}_{hour_key}'
    llm_list_ids = cache.get(llm_cache_key)
    if llm_list_ids is None:
        llm_list_ids = list(LLM.objects.filter(is_public=True).values_list('id', flat=True))
        random.shuffle(llm_list_ids)
        cache.set(llm_cache_key, llm_list_ids, timeout=10)

        # 캐시된 순서대로 LLM 객체 가져오기
    llm_list = list(LLM.objects.filter(id__in=llm_list_ids).prefetch_related('genres'))
    llm_list.sort(key=lambda x: llm_list_ids.index(x.id))
    if request.user.is_authenticated:
        for llm in llm_list:
            try:
                like_obj = LlmLike.objects.get(user=request.user, llm=llm, is_like=True)
                llm.user_has_liked = True
            except LlmLike.DoesNotExist:
                llm.user_has_liked = False
    else:
        for llm in llm_list:
            llm.user_has_liked = False
    context ={
        
        "llm_list": llm_list,
        "LANGUAGE_CODE": language_code,
    }

    return render (request, "home/llm_section.html",context)


from distribute.models import Comment
from home.forms import CommentForm

@login_required
def comment_create(request, llm_id):
    llm = get_object_or_404(LLM, id=llm_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.llm = llm
            # 답글 처리
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent_comment = parent_comment
            comment.save()
    return redirect('home:main', llm.id)

@login_required
def voice_all(request):
    voice = CelebrityVoice.objects.all().order_by("?")
    context = {
        "voice_list": voice

    }
    return render(request, "home/voice_all.html", context)

import json
@csrf_exempt
@login_required
def save_voice(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": _("로그인이 필요합니다.")}, status=401)  

    if request.method == "POST":
        data = json.loads(request.body)
        celebrity_id = data.get("celebrity_id")

        try:
            celeb = CelebrityVoice.objects.get(id=celebrity_id)
        except CelebrityVoice.DoesNotExist:
            return JsonResponse({"error": _("CelebrityVoice가 존재하지 않습니다.")}, status=404)

        voice, created = VoiceList.objects.get_or_create(
            user=request.user,
            celebrity=celeb,
            defaults={
                "voice_name": celeb.name,        
                "voice_id": celeb.celebrity_voice_id,  
                "voice_image": celeb.celebrity_voice_image if celeb.celebrity_voice_image else None,
                "sample_url": celeb.sample_url.url if celeb.sample_url else None 
            }
        )

        if not created:
            return JsonResponse({"status": "exists", "voice_id": voice.voice_id})

        return JsonResponse({"status": "ok", "voice_id": voice.voice_id, "voice_name": voice.voice_name})
    return JsonResponse({"error": _("잘못된 요청입니다.")}, status=400)


from customer_ai.models import Prompt
from django.db.models import Count
from django.shortcuts import get_object_or_404, render

def user_intro(request, user_id):
    user = get_object_or_404(User, id=user_id)

    total_follow_count = User.objects.filter(id=user_id)\
        .annotate(follower_count=Count('follower_set', distinct=True))\
        .order_by('-follower_count')[:12]

    llm_list = LLM.objects.filter(user_id=user_id, is_public=True)
    prompt_list = Prompt.objects.filter(user_id=user_id)

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    else:
        is_following = False

    # user와 팔로우 여부를 같이 리스트로 만들어서 넘김
    user_list = [{
        'user': user,
        'is_following': is_following
    }]

    context = {
        "user_list": user_list,
        "total_follow_count": total_follow_count,
        "llm_list": llm_list,
        "prompt_list": prompt_list,
    }

    return render(request, "home/user_intro.html", context)



def soon(request):
    return render(request, "home/soon.html")


import secrets
import string
from django.contrib.auth.decorators import login_required

def generate_code(length=10):
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


from django.utils import timezone
from user_auth.models import Referral, Coupon
@login_required
def invite(request):
    gift_list = Gift.objects.all()

    invite_code = request.session.get('invite_code')  # 기존 세션 코드
    invite_link = None

    if request.method == "POST":
        # 새 코드 생성
        invite_code = generate_code()
        request.session['invite_code'] = invite_code
        invite_link = request.build_absolute_uri(f"/")

        # Referral DB에 저장 (inviter = 현재 사용자)
        Referral.objects.create(
            inviter=request.user,
            code=invite_code,
            is_active=True,
            created_at=timezone.now()
        )

    else:
        if invite_code:
            invite_link = request.build_absolute_uri(f"/invite/?code={invite_code}")

    context = {
        "gift_list": gift_list,
        "invite_code": invite_code,
        "invite_link": invite_link,
    }
    return render(request, "home/invite.html", context)



def bad_request(request, exception):
    return render(request, "error/400.html", status=400)

def permission_denied(request, exception):
    return render(request, "error/403.html", status=403)

def page_not_found(request, exception):
    return render(request, "error/404.html", status=404)

def server_error(request):
    return render(request, "error/500.html", status=500)