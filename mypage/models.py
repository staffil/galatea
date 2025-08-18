from home.models import Users
from django.db import models
from customer_ai.models import LLM

# 장르 테이블
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    genre_image = models.ImageField(upload_to='uploads/genre_images/', null=True, blank=True)
    color = models.CharField(max_length=10, default='#FFF', verbose_name='태그 넣을떄 색깔')

    class Meta:
        db_table = 'genres'
        verbose_name = '장르'

    def __str__(self):
        return self.name 
