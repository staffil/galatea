from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('kakaopay', 'Kakao Pay'),
        ('tosspay', 'Toss Pay'),
    ]
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('pending', 'Pending'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    imp_uid = models.CharField(max_length=100)  # 아임포트 결제 고유 ID
    merchant_uid = models.CharField(max_length=100)  # 가맹점에서 생성한 주문번호
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}원"
