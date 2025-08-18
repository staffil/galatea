from django.db import models
from mypage.models import Genre
from django.conf import settings

# 댓글 테이블
# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    llm = models.ForeignKey('customer_ai.LLM', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='댓글')
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT,  # 삭제를 막고 싶을 때 사용
        related_name='replies',
        verbose_name='답글 대상 댓글',
    )

    class Meta:
        db_table = 'comment'
        verbose_name = 'AI 대한 댓글창',
        ordering = ['-created_at']







# 기존 llm 이미지 테이블
class LlmBackgroundImage(models.Model):
    llm = models.ForeignKey('customer_ai.LLM', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    default_img = models.ImageField(upload_to='uploads/default_img/', null=True, blank=True)
    class Meta:
        db_table = 'llm_background_image'
        verbose_name = 'llm 배경사진'