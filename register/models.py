from django.db import models
from django.utils import timezone
from django.conf import settings





# UserSession 테이블
class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255)
    device_info = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_session'
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'



from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
# 팔로우 테이블
class Follow(models.Model):
    follower = models.ForeignKey(User,related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(User,related_name='follower_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        db_table= 'follow'
        verbose_name = '팔로우 목록'

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import timezone
from django.contrib.postgres.fields import JSONField  # PostgreSQL 기준
# MySQL 사용 시 JSONField는 django.db.models.JSONField 사용 가능 (Django 3.1 이상)

class SocialApp(models.Model):
    PROVIDER_CHOICES = [
        ('github', 'GitHub'),
        ('google', 'Google'),
    ]
    
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    name = models.CharField(max_length=150)
    client_id = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    key = models.CharField(max_length=255, blank=True)
    sites = models.ManyToManyField(Site, related_name='register_socialapps')
    
    def __str__(self):
        return f"{self.provider} - {self.name}"


class SocialAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='register_socialaccounts')
    provider = models.CharField(max_length=50, choices=SocialApp.PROVIDER_CHOICES)
    uid = models.CharField(max_length=255)  # 소셜 제공자의 고유 사용자 ID
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)
    extra_data = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.user} ({self.provider})"

class SocialToken(models.Model):
    app = models.ForeignKey(SocialApp, on_delete=models.CASCADE)
    account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE)
    token = models.TextField()
    token_secret = models.TextField(blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Token for {self.account.user} ({self.app.provider})"
