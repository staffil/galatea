# register/adapter.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from django.conf import settings

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_app(self, request, provider, client_id =None):
        site_id = getattr(settings, "SITE_ID", 1)
        apps = SocialApp.objects.filter(provider=provider, sites__id=site_id)
        if apps.exists():
            return apps.first()  # 첫 번째 SocialApp만 사용
        return None
