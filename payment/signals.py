from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from payment.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
