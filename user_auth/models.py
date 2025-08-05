from django.db import models
from home.models import Users
from mypage.models import Voice, LLM

class Celebrity(models.Model):
    celebrity_name = models.CharField(max_length=100)
    celebrity_prompt = models.TextField()
    description = models.TextField()
    celebrity_image = models.ImageField(upload_to='uploads/celebrity_images/', null=True, blank=True)
    celebrity_voice_id = models.CharField(max_length=200, null=True, blank=True)


    class Meta:
        db_table = 'celebrity'


class Conversation(models.Model):
    llm = models.ForeignKey(LLM, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    user_message = models.TextField(null=True, blank=True)
    llm_response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversation'


class Authority(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        db_table = 'authority'


class UserAuth(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_auth'
        unique_together = ('user', 'authority')
