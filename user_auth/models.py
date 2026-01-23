from django.db import models
from celebrity.models import Celebrity
from django.conf import settings

# 관리자 테이블
class Authority(models.Model):
    name = models.CharField(max_length=40, verbose_name='관리자 명(ROLE_ADMIN)')
    nickname = models.TextField(default='관리자')

    class Meta:
        db_table = 'authority'
        verbose_name = '관리자'
# userAuth 테이블
class UserAuth(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    authority = models.ForeignKey('Authority', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_auth'
        unique_together = (('user', 'authority'),)
        verbose_name = 'User Authority'
        verbose_name_plural = 'User Authorities'

        
# 쿠폰 테이블
class Coupon(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, verbose_name='쿠폰 코드')
    description = models.TextField(verbose_name='쿠폰 설명')
    start_day = models.DateTimeField(verbose_name='쿠폰 시작일')
    end_day = models.DateTimeField(verbose_name='쿠폰 만료일')
    is_activate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'coupon'


# 친구 초대 기록 
class Referral(models.Model):
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_invites")
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_invites", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=10, blank=True, null=True) 
    is_active = models.BooleanField(default=True) 

    class Meta:
        db_table = 'referral'
        unique_together = ("invitee",)


# FAQ 테이블
class Faq(models.Model):
    title = models.CharField(max_length=1000)
    content = models.TextField()
    faq_img = models.ImageField(upload_to='uploads/gift/', null=True, blank=True)


    class Meta:
        db_table = 'faq'
        verbose_name = 'FAQ'

# 선물 광고 테이블
class Gift(models.Model):
    title = models.CharField(max_length=200, verbose_name='title 은 관리자에서 빨리 찾을 수 있게 일단 만듦')
    gift_img = models.ImageField(upload_to='uploads/gift/', null=True, blank=True)

    class Meta:
        db_table = 'gift'
        verbose_name = '이벤트'





# 뉴스 테이블
class News(models.Model):
    title = models.CharField(max_length=1000)
    news_img = models.ImageField(upload_to='uploads/news/', null=True, blank=True)
    news_description = models.TextField(verbose_name='해당 new 설명')
    link = models.CharField(max_length=500, verbose_name='이벤트나 어떤 llm 모델을 소개해주고 싶을떄 소개하는 페이지 아래 칸에 넣을 url 경로')

    class Meta:
        db_table = 'news'
        verbose_name = '뉴스'


# 요구사항 테이블
class Requests(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    title = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(null=True, blank=True)
    is_secret = models.BooleanField(default=False)

    class Meta:
        db_table = 'requests'
        verbose_name = '요청 사항'

# 공지사항 테이블
from home.models import Users
class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # 공지 활성화 여부

    class Meta:
        db_table = 'notice'
        verbose_name = '공지사항'

    def __str__(self):
        return self.title


