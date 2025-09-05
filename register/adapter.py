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
