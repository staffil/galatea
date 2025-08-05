# register/views.py
from django.shortcuts import render, redirect
from home.models import Users
from register.form import SignupForm, LoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login as auth_login


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


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("로그인 성공")
                auth_login(request, user)
                return redirect('main')
            else:
                form.add_error(None, "아이디 또는 비밀번호가 올바르지 않습니다.")
    else:
        form = LoginForm()
    return render(request, 'register/login.html', {'form': form})
