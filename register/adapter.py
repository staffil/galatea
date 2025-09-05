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
    
    def pre_social_login(self, request, sociallogin):
        """
        소셜 로그인 시 기존 이메일 계정이 있으면
        자동으로 연결하고 '계속' 화면 건너뛰기
        """
        if sociallogin.is_existing:
            return  # 이미 연결된 계정이면 그냥 넘어감

        try:
            # 이메일로 기존 사용자 조회
            email = sociallogin.user.email
            user = Users.objects.get(email=email)
            sociallogin.connect(request, user)  # 기존 계정과 연결
        except Users.DoesNotExist:
            pass  # 새 계정이면 그대로 진행