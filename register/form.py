from django import forms
from home.models import Users
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _  # import 추가


class SignupForm(forms.Form):
    username = forms.CharField(
        label=_('아이디'),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('아이디를 입력하세요')}),
    )
    nickname = forms.CharField(
        label=_('닉네임'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('닉네임 입력하세요')}),
    )
    password1 = forms.CharField(
        label=_('비밀번호'),
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('비밀번호 입력하세요()')}),
    )
    password2 = forms.CharField(
        label=_('비밀번호 확인'),
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('비밀번호 재입력')}),
    )
    email = forms.EmailField(
        label=_('이메일'),
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': _('이메일 입력')}),
    )
    phone = forms.CharField(
        label=_('전화번호'),
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('전화번호 입력 (- 포함)')}),
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
            self.add_error('username', _('아이디는 필수 입력입니다.'))
        elif Users.objects.filter(username=username).exists():
            self.add_error('username', _('이미 존재하는 아이디입니다.'))

        if not nickname:
            self.add_error('nickname', _('닉네임은 필수 입력입니다.'))

        if not password1:
            self.add_error('password1', _('비밀번호는 필수 입력입니다.'))
        else:
            pattern = r'^(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,}$'
            if not re.match(pattern, password1):
                self.add_error('password1', _("형식이 맞지 않습니다. 비밀번호는 소문자 최소 1개, 숫자 최소 1개,특수문자 최소 1개 이상이여야 합니다. ex): abcd1234! "))

        if not password2:
            self.add_error('password2', _('비밀번호 확인은 필수 입력입니다.'))

        if password1 and password2 and password1 != password2:
            self.add_error('password2', _('비밀번호가 일치하지 않습니다.'))

        if not email:
            self.add_error('email', _('이메일은 필수 입력입니다.'))
        elif Users.objects.filter(email=email).exists():
            self.add_error('email', _('이미 존재하는 이메일입니다.'))

        if not phone:
            self.add_error('phone', _('전화번호는 필수 입력입니다.'))
        else:
            pattern = r'^\d{3}-\d{4}-\d{4}$'  # 000-0000-0000 형식 검사
            if not re.match(pattern, phone):
                self.add_error('phone', _('전화번호 형식이 올바르지 않습니다. (예: 010-1234-5678)'))


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('아이디'),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _('아이디를 입력하세요')})
    )
    password = forms.CharField(
        label=_("비밀번호"),
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": _("비밀번호 입력하세요")})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            self.add_error('username', _("아이디를 입력해 주세요"))
            return

        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            self.add_error('username', _("존재하지 않는 아이디입니다."))
            return

        if not password:
            self.add_error('password', _("비밀번호를 입력하세요."))
        elif not check_password(password, user.password):
            self.add_error('password', _("비밀번호가 일치하지 않습니다."))
