from django.db import models

# 대화 테이블
from django.db import models

from django.db import models
from django.conf import settings
from django.utils import timezone
from makeVoice.models import VoiceList

class Conversation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 커스텀 유저 모델을 안전하게 참조
        on_delete=models.CASCADE,
        related_name='conversations'
    )
    llm = models.ForeignKey('customer_ai.LLM', on_delete=models.CASCADE)
    user_message = models.TextField()
    llm_response = models.TextField()
    response_audio = models.FileField(upload_to='audio/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'conversation'
        verbose_name = '대화목록'

    def __str__(self):
        return f"Conversation {self.id} by {self.user}"





# llm 좋아요 테이블
class LlmLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    llm = models.ForeignKey('customer_ai.LLM', on_delete=models.CASCADE, related_name='like')
    is_like = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'llm_like'
        verbose_name = 'AI 좋아요'
        unique_together = ('user', 'llm')

#llm 테이블
class LLM(models.Model):
    MODEL_CHOICES = [
        ('gpt-3.5-turbo', 'GPT-3.5 Turbo'),
        ('gpt-4o-mini', 'GPT-4o Mini'),
        ('gpt-4o', 'GPT-4o'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='llm_set')
    voice = models.ForeignKey('makeVoice.VoiceList', on_delete=models.CASCADE, null=True, blank=True, related_name='llms')
    genres = models.ManyToManyField('mypage.Genre', related_name='llms', blank=True)

    name = models.CharField(max_length=100, verbose_name='user 가 지정한 LLM 이름')
    prompt = models.TextField(verbose_name='user 가 지정한 프롬프트')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='user 가 LLM 을 만든 시기')
    update_at = models.DateTimeField(null=True, blank=True, auto_now=True, verbose_name='user 가 프롬프트, 목소리 변형을 했을 경우 나중에 문제가 생겼을때 원인을 찾을 수 있음')
    llm_image = models.ImageField(upload_to='uploads/llm_images/', null=True, blank=True)
    response_mp3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='해당 보이스를 저장할 수 있는 mp3 파일 -> 목소리는 ai가 대답할 떄마다 기록이 덮어씌워짐')
    model = models.CharField(max_length=20, choices=MODEL_CHOICES, default='gpt-3.5-turbo', verbose_name='gpt 모델 중 하나를 선택해서 사용할 수 있음')
    language = models.CharField(max_length=10, default='en')
    temperature = models.FloatField(default=1.0)
    stability = models.FloatField(default=0.5)
    speed = models.FloatField(default=1.0)
    style = models.FloatField(default=0.5)
    is_public = models.BooleanField(default=False, verbose_name='해당 LLM 을 공유 할 것인가?')
    title = models.CharField(max_length=1000, null=True)
    description = models.TextField(null=True, blank=True, verbose_name='해당 LLM 이 공유될떄 실행')
    llm_like_count = models.IntegerField(default=0, verbose_name='llm이 받은 좋아요 갯수')
    llm_background_image = models.ImageField(upload_to='uploads/llm_background_images/', null=True, blank=True)
    invest_count = models.IntegerField(default=0)


    class Meta:
        db_table = 'LLM'
        verbose_name = 'ai 정보'

        



# 프롬프트 테이블 
class Prompt(models.Model):
    PROMPT_TYPE_CHOICES = [
        ('text', '일반 프롬프트'),
        ('voice', '목소리 프롬프트'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prompt_title = models.CharField(max_length=100, verbose_name="프롬프트 제목 적는칸")
    prompt = models.TextField(verbose_name="프롬프트 적는 칸")
    prompt_type = models.CharField(max_length=10, choices=PROMPT_TYPE_CHOICES, default='text')
    created_at = models.DateTimeField(auto_now_add=True)    

    class Meta:
        db_table = "prompt"
        verbose_name = 'prompt 정보'

        

