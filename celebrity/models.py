from django.db import models

# Create your models here.

# celebrity llm 테이블
class Celebrity(models.Model):
    celebrity_voice_id = models.CharField(max_length=200, verbose_name='celebrity voiceid')
    celebrity_name = models.CharField(max_length=100)
    celebrity_prompt = models.TextField()
    description = models.TextField()
    celebrity_image = models.ImageField(upload_to='uploads/celebrity_images/', null=True, blank=True)
    class Meta:
        db_table = 'celebrity'
        verbose_name = 'celebrity 커스텀'

# celebirty voice 테이블
class CelebrityVoice(models.Model):
    name = models.CharField(max_length=200, verbose_name='보이스 이름')
    sample_url = models.FileField(upload_to='voices/',  verbose_name='보이스 목소리 url', blank=True, null=True)
    celebrity_voice_id = models.CharField(max_length=200)
    celebrity_voice_image = models.ImageField(upload_to='uploads/celebrity_voice_image/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'celebrity_voice'
        verbose_name = 'celebrity 보이스 목록'