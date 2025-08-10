from modeltranslation.translator import translator, TranslationOptions
from user_auth.models import Celebrity

class CelebrityTranslationOptions(TranslationOptions):
    fields = ('celebrity_name', 'description',) 

translator.register(Celebrity, CelebrityTranslationOptions)
