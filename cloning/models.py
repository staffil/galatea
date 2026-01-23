from django.db import models
from django.conf import settings

class CloningAgreement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name="유저"
    )
    consent_voice = models.BooleanField(default=False, verbose_name="본인 음성 클로닝 동의")
    consent_third = models.BooleanField(default=False, verbose_name="타인 음성 사용 책임 인지")
    consent_share = models.BooleanField(default=False, verbose_name="클로닝 음성 공유 금지")
    consent_date = models.DateTimeField(auto_now_add=True, verbose_name="동의 일시")
    voice_text = models.TextField(verbose_name='동의서 전문(voice text)')
    third_text = models.TextField(verbose_name='동의서 전문(third text)')
    share_text = models.TextField(verbose_name='동의서 전문(share text)')

    class Meta:
        db_table = 'cloning_agreement'
        verbose_name = "보이스 클로닝 동의 항목"
        

    def __str__(self):
        return f"{self.user} - {self.consent_date}"