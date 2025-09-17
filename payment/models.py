from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# 결제 수단 테이블
class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)  
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    payment_image = models.ImageField( null=True, blank=True)

    class Meta:
        db_table = 'payment_method'
        verbose_name = '결제 수단'
        verbose_name_plural = '결제 수단들'

    def __str__(self):
        return self.name
    

class PaymentRank(models.Model):
    rankname = models.CharField(max_length=100, verbose_name='결제 등급', unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='등급에 따른 가격')
    daller_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='등급에 따른 가격(달러)')
    voicetime = models.CharField(max_length=100, verbose_name='가격에 따른 음성 시간')
    freetoken = models.IntegerField(null=True, verbose_name='등급에 따른 무료 토큰 횟수')
    color = models.CharField(max_length=100,  default="#FFF", verbose_name='등급에 따른 색깔')


    class Meta:
        db_table = 'payment_rank'
        verbose_name = '결제 등급'
        verbose_name_plural = '결제 등급'


# 결제 테이블
class Payment(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('pending', 'Pending'),
        ('refunded', 'Refunded'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='유저 id 정보')
    payment_rank = models.ForeignKey(PaymentRank, on_delete=models.PROTECT, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='실제 결제된 금액 기록')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    paid_at = models.DateTimeField(auto_now_add=True, verbose_name='결제한 날짜')
    imp_uid = models.CharField(max_length=100, null=True, blank=True, verbose_name='결제 번호')
    merchant_uid = models.CharField(max_length=100, null=True, blank=True, verbose_name='주문번호')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='결제 방식')
    apply_num = models.CharField(max_length=50, null=True, blank=True, verbose_name='PG 승인 번호')
    currency = models.CharField(max_length=10, default='KRW', verbose_name='결제 통화 기록')
    refund_reason = models.TextField(null=True, blank=True, verbose_name='환불 사유')
    customer_uid = models.CharField(max_length=100,  null=True, blank=True, verbose_name="PG 사 발급 토큰")

    class Meta:
        db_table = 'payment'
        verbose_name = '결제 수단, 관리'




# 총 토큰 테이블
class TotalToken(models.Model):
    total_tokens_used = models.BigIntegerField(default=0)
    total_llm_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'total_token'
        verbose_name = 'Total Token'
        verbose_name_plural = 'Total Tokens'

from decimal import Decimal

# 토큰 히스토리 테이블
class TokenHistory(models.Model):
    CHARGE = 'charge'
    CONSUME = 'consume'
    CHANGE_TYPE_CHOICES = [
        (CHARGE, 'Charge'),
        (CONSUME, 'Consume'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPE_CHOICES)
    amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_voice_generated = models.IntegerField(default=0)  


    class Meta:
        db_table = 'token_history'
        verbose_name = 'Token History'
        verbose_name_plural = 'Token Histories'

    def save(self, *args, **kwargs):
        token_obj, _ = Token.objects.get_or_create(user=self.user)
        if self.change_type == self.CHARGE:
            token_obj.total_token += self.amount
        elif self.change_type == self.CONSUME:
            if token_obj.remaining_tokens() < self.amount:
                raise ValueError("Not enough tokens to consume")
            token_obj.token_usage += self.amount
        token_obj.save()
        super().save(*args, **kwargs)



from django.db import models
from django.contrib.auth.models import User

class Token(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True)
    total_token = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    token_usage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table= 'token'
        verbose_name = 'TOKEN'
        verbose_name_plural = "TOKENS"

    def __str__(self):
        return f"Token(user={self.user_id}, total={self.total_token}, usage={self.token_usage})"
    
    def remaining_tokens(self):
        return self.total_token - self.token_usage
    
    def consume(self, amount):
        if self.remaining_tokens() < amount:
            return False
        self.token_usage += amount
        self.save()
        return True
    
    


class PaymentStats(models.Model):
    total_payments = models.PositiveIntegerField(default=0, verbose_name="총 결제 횟수")
    success_count = models.PositiveIntegerField(default=0, verbose_name="성공 결제 횟수")
    failure_count = models.PositiveIntegerField(default=0, verbose_name="실패 결제 횟수")
    pending_count = models.PositiveIntegerField(default=0, verbose_name="대기 결제 횟수")
    refunded_count = models.PositiveIntegerField(default=0, verbose_name="환불 횟수")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_stats'
        verbose_name = '결제 통계'
        verbose_name_plural = '결제 통계'


