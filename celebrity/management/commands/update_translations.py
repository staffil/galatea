from django.core.management.base import BaseCommand
from user_auth.models import Celebrity

class Command(BaseCommand):
    help = 'Copy existing celebrity fields to translation fields for multiple languages'

    def handle(self, *args, **kwargs):
        for obj in Celebrity.objects.all():
            obj.celebrity_name_en = obj.celebrity_name
            obj.description_en = obj.description

            obj.celebrity_name_fr = obj.celebrity_name
            obj.description_fr = obj.description

            obj.celebrity_name_ar = obj.celebrity_name
            obj.description_ar = obj.description

            obj.celebrity_name_ja = obj.celebrity_name
            obj.description_ja = obj.description

            obj.celebrity_name_zh = obj.celebrity_name
            obj.description_zh = obj.description

            obj.celebrity_name_hi = obj.celebrity_name
            obj.description_hi = obj.description

            obj.save()
        self.stdout.write(self.style.SUCCESS('Translations fields updated successfully for all languages.'))
