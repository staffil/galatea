from django.db import models
from mypage.models import Voice
from home.models import Users
# Create your models here.
def input_voice_id():
    return Voice.objects.all()


class VoiceList(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    voice_id = models.CharField(max_length=200, unique=True)
    sample_url = models.URLField(max_length=500, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    voice_name = models.CharField(max_length=400)

    class Meta:
        db_table = 'voice_list'

