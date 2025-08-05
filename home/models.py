from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    nickname = models.CharField(max_length=100, unique=True)
    phonenumber = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)  # AbstractUser는 date_joined 필드 기본 제공
    user_image = models.ImageField(upload_to='uploads/profile_images/', null=True, blank=True)
    email = models.CharField(max_length=400, unique=False)


    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
