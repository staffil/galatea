# register/forms.py
from django import forms
from home.models import Users
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import check_password  # 중요


class SignupForm(forms.Form):
    username = forms.CharField(
        label='아이디',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '아이디를 입력하세요'}),
    )
    nickname = forms.CharField(
        label='닉네임',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '닉네임 입력하세요'}),
    )
    password1 = forms.CharField(
        label='비밀번호',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 입력하세요()'}),
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 재입력'}),
    )
    email = forms.EmailField(
        label='이메일',
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': '이메일 입력'}),
    )
    phone = forms.CharField(
        label='전화번호',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '전화번호 입력 (- 포함)'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        nickname = cleaned_data.get('nickname')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')

        if not username:
            self.add_error('username', '아이디는 필수 입력입니다.')
        elif Users.objects.filter(username=username).exists():
            self.add_error('username', '이미 존재하는 아이디입니다.')

        if not nickname:
            self.add_error('nickname', '닉네임은 필수 입력입니다.')

        if not password1:
            self.add_error('password1', '비밀번호는 필수 입력입니다.')
        else:
            pattern = r'^(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,}$'
            if not re.match(pattern, password1):
                self.add_error('password1',"형식이 맞지 않습니다. 비밀번호는 소문자 최소 1개, 숫자 최소 1개,특수문자 최소 1개 이상이여야 합니다. ex): abcd1234! ")

        if not password2:
            self.add_error('password2', '비밀번호 확인은 필수 입력입니다.')
        

        if password1 and password2 and password1 != password2:
            self.add_error('password2', '비밀번호가 일치하지 않습니다.')

        if not email:
            self.add_error('email', '이메일은 필수 입력입니다.')
        elif Users.objects.filter(email=email).exists():
            self.add_error('email', '이미 존재하는 이메일입니다.')

        if not phone:
            self.add_error('phone', '전화번호는 필수 입력입니다.')
        else:
            pattern = r'^\d{3}-\d{4}-\d{4}$'  # 000-0000-0000 형식 검사
            if not re.match(pattern, phone):
                self.add_error('phone', '전화번호 형식이 올바르지 않습니다. (예: 010-1234-5678)')

class LoginForm(forms.Form):
    username = forms.CharField(
        label='아이디',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": '아이디를 입력하세요'})
    )
    password = forms.CharField(
        label="비밀번호",
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 입력하세요"})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            self.add_error('username', "아이디를 입력해 주세요")
            return

        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            self.add_error('username', "존재하지 않는 아이디입니다.")
            return

        if not password:
            self.add_error('password', "비밀번호를 입력하세요")
        elif not check_password(password, user.password):
            self.add_error('password', "비밀번호가 일치하지 않습니다.")