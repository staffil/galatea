from django.db import models

class AIConfig(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    prompt = models.TextField(blank=True, null=True)
    stability = models.FloatField(default=0)
    similarity = models.FloatField(default=0)
    style = models.FloatField(default=0)
    language = models.CharField(max_length=20, blank=True, null=True)
    voice_id = models.CharField(max_length=100, blank=True, null=True)
    speed = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
