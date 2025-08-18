# register/views.py
from django.shortcuts import render, redirect
from home.models import Users
from register.form import SignupForm, LoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.utils.translation import get_language


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = Users(
                username=form.cleaned_data['username'],
                nickname=form.cleaned_data['nickname'],
                password=make_password(form.cleaned_data['password1']),
                email=form.cleaned_data['email'],
                phonenumber=form.cleaned_data['phone']
            )
            user.save()
            return redirect('register:login')
    else:
        form = SignupForm()

    return render(request, 'register/signup.html', {'form': form})


def login_view(request):
    language = get_language()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("로그인 성공")
                auth_login(request, user)
                return redirect('home:main')
            else:
                form.add_error(None, "아이디 또는 비밀번호가 올바르지 않습니다.")
    else:
        form = LoginForm()
    return render(request, 'register/login.html', {
        'form': form,
        'google_client_id': settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id'],
        "LANGUAGE_CODE": language,
        })
import os
import json
import requests
from django.contrib.auth import login, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

User = get_user_model()

GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


def verify_google_token(token):
    try:
        response = requests.get(
            'https://oauth2.googleapis.com/tokeninfo',
            params={'id_token': token},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print("Google tokeninfo request failed:", e)
        return None

    print(f"Google aud: '{data.get('aud')}' vs GOOGLE_CLIENT_ID: '{GOOGLE_CLIENT_ID}'")
    print("Google tokeninfo data:", data)

    if data.get('aud') != GOOGLE_CLIENT_ID:
        print("Client ID mismatch:", data.get('aud'), GOOGLE_CLIENT_ID)
        return None
    return data


@csrf_exempt
def google_login(request):
    print("google_login 호출, method:", request.method)
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST 요청만 허용'}, status=400)
    print('IJEJFIJEIFJIEJFIFIFIEJFIFJIEFJEIFJIFJIFJEIF')
    try:
        body = json.loads(request.body)
        print("Request body:", body)
        token = body.get('token')
        if not token:
            return JsonResponse({'success': False, 'error': '토큰이 없습니다'}, status=400)

        user_info = verify_google_token(token)
        if not user_info:
            return JsonResponse({'success': False, 'error': '유효하지 않은 토큰'}, status=400)

        email = user_info.get('email')
        name = user_info.get('name')
        google_id = user_info.get('sub')

        print(f"Google 로그인 정보 - email: {email}, name: {name}, google_id: {google_id}")

        # 필수 필드 nickname, phonenumber 임시값으로 넣기
        user, created = User.objects.get_or_create(
            username=google_id,
            defaults={
                'email': email,
                'first_name': name,
                'nickname': email.split('@')[0],  # 닉네임 임시로 이메일 앞부분 사용
                'phonenumber': '',  # 빈 문자열로 임시 지정 (null=False이기 때문)
            }
        )
        login(request, user)
        print("로그인 성공, user:", user)

        return JsonResponse({'success': True, 'created': created})

    except Exception as e:
        import traceback
        print("Exception in google_login:", e)
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
