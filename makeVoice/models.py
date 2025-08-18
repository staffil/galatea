
# vocie 리스트 테이블
from django.db import models
from home.models import Users

from django.utils import timezone
from django.conf import settings

class VoiceList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    llm = models.ForeignKey('customer_ai.LLM', on_delete=models.CASCADE, null=True, blank=True, default=None)
    sample_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    voice_name = models.CharField(max_length=100)
    voice_image = models.ImageField(upload_to='uploads/voice_images/HOME v.png/', null=True, blank=True, default="uploads/voice_images/HOMEv.png/") 
    is_public = models.BooleanField(default=False, null=True, blank=True)
    voice_id = models.CharField(max_length=200)
    voice_like_count = models.IntegerField(default=0, verbose_name='보이스가 받은 좋아요 갯수')

    class Meta:
        db_table = "voice_list"
        verbose_name = "voice 리스트"

    def __str__(self):
        return self.voice_name
    


# 보이스 좋아요 테이블

class VoiceLike(models.Model):
    id = models.AutoField(primary_key=True)
    voice_list = models.ForeignKey('VoiceList', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        db_table = 'voice_like'
        verbose_name = 'voice 좋아요'

    def __str__(self):
        return f"VoiceLike by {self.user} on {self.voice_list}"
