from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
# user 테이블
class Users(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    nickname = models.CharField(max_length=100, default='user',null=False,)
    phonenumber = models.CharField(max_length=30)
    # name = models.CharField(max_length=100)
    # country = models.CharField(max_length=3)
    # postal_code = models.CharField(max_length=30)
    # address_line1 = models.CharField(max_length=255)
    # address_line2 = models.CharField(max_length=255, null=True, blank=True)
    user_image = models.ImageField(upload_to='uploads/profile_images/', null=True, blank=True,max_length=500,)
    oauth_provider = models.CharField(max_length=20, choices=[('google', 'Google'), ('microsoft', 'Microsoft'), ('github', 'GitHub')], null=True, blank=True)
    oauth_uid = models.CharField(max_length=200, null=True, blank=True)
    access_token = models.CharField(max_length=500, null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('banned', 'Banned')], default='active')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    follow_count = models.IntegerField(default=0, verbose_name='팔로우 수')
    followers = models.ManyToManyField('self', symmetrical=False, blank=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = '사용자'

    def __str__(self):
        return self.email
