from django.db import models
from home.models import Users

# Create your models here.


class Voice(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    voice_id = models.CharField(max_length=200, unique=True)
    update_at = models.DateTimeField(auto_now=True)
    preview_url = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        db_table = "voice"
class LLM(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    voice = models.ForeignKey(Voice, on_delete=models.CASCADE)
    celebrity = models.ForeignKey('user_auth.Celebrity', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    response_mp3 = models.CharField(max_length=255, null=True, blank=True)
    llm_image = models.ImageField(upload_to='uploads/llm_images/', null=True, blank=True)
    language = models.CharField(max_length=10, default='en')
    temperature = models.FloatField(default=1.0)
    stability = models.FloatField(default=0.5)
    speed = models.FloatField(default=1.0, null=True, blank=True)
    style = models.FloatField(default=0.5)

    model = models.CharField(
        max_length=20,
        choices=[
            ('gpt-3.5-turbo', 'GPT-3.5 Turbo'),
            ('gpt-4o-mini', 'GPT-4o Mini'),
            ('gpt-4o', 'GPT-4o'),
        ],
        default='gpt-3.5-turbo'
    )
    class Meta:
        db_table = 'llms'

    def __str__(self):
        return self.name





