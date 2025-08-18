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

