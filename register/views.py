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


from django.contrib.sites.models import Site
from django.urls import reverse
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.providers.google.views import OAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialApp
def login_view(request):
    language = get_language()
    site = Site.objects.get(id=settings.SITE_ID)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home:main')
            else:
                form.add_error(None, "아이디 또는 비밀번호가 올바르지 않습니다.")
    else:
        form = LoginForm()

    try:
        google_url = reverse('socialaccount_login', args=['google'])
        github_url = reverse('socialaccount_login', args=['github'])
    except Exception as e:
        google_url = '#'
        github_url = '#'
        print("Reverse Error:", e)

    return render(request, 'register/login.html', {
        'form': form,
        'site': site,
        'google_login_url': google_url,
        'github_login_url': github_url,
        "LANGUAGE_CODE": language,
    })

from allauth.socialaccount.models import SocialAccount

def get_github_name(user):
    try:
        account = SocialAccount.objects.get(user=user, provider='github')
        return account.extra_data.get('name')
    except SocialAccount.DoesNotExist:
        return None

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def google_callback(request):
    if request.method == 'POST':
        credential = request.POST.get('credential')
        # JWT 토큰 검증 및 사용자 생성/로그인 처리
        # (구글 라이브러리로 JWT 디코딩 필요)
        return JsonResponse({'success': True})
    



#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# 앱 전용

def signup_app(request):
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
            return redirect('register:login_app')
    else:
        form = SignupForm()

    return render(request, 'register/app/signup_app.html', {'form': form})



def login_app(request):
    language = get_language()
    site = Site.objects.get(id=settings.SITE_ID)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home:main_app')
            else:
                form.add_error(None, "아이디 또는 비밀번호가 올바르지 않습니다.")
    else:
        form = LoginForm()

    try:
        google_url = reverse('socialaccount_login', args=['google'])
        github_url = reverse('socialaccount_login', args=['github'])
    except Exception as e:
        google_url = '#'
        github_url = '#'
        print("Reverse Error:", e)

    return render(request, 'register/app/login_app.html', {
        'form': form,
        'site': site,
        'google_login_url': google_url,
        'github_login_url': github_url,
        "LANGUAGE_CODE": language,
    })
