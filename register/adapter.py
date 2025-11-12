# register/adapter.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from django.conf import settings

class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def get_app(self, request, provider, **kwargs):
        """
        Provider와 SITE_ID로 SocialApp을 찾음.
        중복이 있어도 첫 번째 앱만 반환.
        """
        site_id = getattr(settings, "SITE_ID", 1)
        apps = SocialApp.objects.filter(provider=provider, sites__id=site_id)
        if apps.exists():
            return apps.first()
        return None

    def is_open_for_signup(self, request, sociallogin):
        """
        True이면 자동으로 회원가입 가능
        """
        return True

    def populate_user(self, request, sociallogin, data):
        """
        OAuth 데이터로 사용자 객체를 채움
        """
        user = super().populate_user(request, sociallogin, data)

        # email에서 username 자동 생성
        if data.get('email'):
            base_username = data['email'].split('@')[0]
            username = base_username
            counter = 1
            from home.models import Users
            while Users.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            user.username = username
            user.nickname = username

        # phonenumber는 빈 문자열
        user.phonenumber = ''

        return user

    def save_user(self, request, sociallogin, form=None):
        """
        소셜 로그인 후 사용자 저장 시 호출됨
        form=None이면 자동으로 가입됨
        """
        user = super().save_user(request, sociallogin, form)

        # 필수 필드 자동 채우기
        if not user.username:
            # email에서 username 생성
            user.username = user.email.split('@')[0]
            # 중복 방지
            base_username = user.username
            counter = 1
            from home.models import Users
            while Users.objects.filter(username=user.username).exclude(pk=user.pk).exists():
                user.username = f"{base_username}{counter}"
                counter += 1

        if not user.phonenumber:
            user.phonenumber = ''  # 빈 문자열로 설정

        if not user.nickname:
            user.nickname = user.username or 'user'

        user.save()
        return user
    def pre_social_login(self, request, sociallogin):
        print("=== pre_social_login triggered ===")


        if sociallogin.is_existing:
            return
        
        try:
            from home.models import Users  # 커스텀 사용자 모델 import
            user = Users.objects.get(email__iexact=sociallogin.account.extra_data['email'])
            sociallogin.connect(request, user)
        except Users.DoesNotExist:
            pass