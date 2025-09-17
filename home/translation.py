from modeltranslation.translator import translator, TranslationOptions
from celebrity.models import Celebrity
from celebrity.models import CelebrityVoice
from mypage.models import Genre
from user_auth.models import News, Coupon, Notice, Gift ,Faq
from cloning.models import CloningAgreement
from payment.models import PaymentRank


class CelebrityTranslationOptions(TranslationOptions):
    fields = ('celebrity_name', 'description',) 

translator.register(Celebrity, CelebrityTranslationOptions)


class CelebrityVoiceTranslationsOption(TranslationOptions):
    fields = ('name',)
translator.register(CelebrityVoice, CelebrityVoiceTranslationsOption)


class GenreTranslationsOption(TranslationOptions):
    fields = ("name",)
translator.register(Genre, GenreTranslationsOption)

class NewsTranslationsOption(TranslationOptions):
    fields = ("title", "news_img", "news_description",)
translator.register(News, NewsTranslationsOption)



class CouponTranslationsOption(TranslationOptions):
    fields = ("description",)
translator.register(Coupon, CouponTranslationsOption)

class NoticeTranslationsOption(TranslationOptions):
    fields = ('title', 'content', )
translator.register(Notice, NoticeTranslationsOption)


class FAQTranslationsOption(TranslationOptions):
    fields = ('title', 'content',)
translator.register(Faq, FAQTranslationsOption)

class GiftTranslationsOption(TranslationOptions):
    fields = ('title', "gift_img",)
translator.register(Gift, GiftTranslationsOption)



class CloningAgreementTranslationsOption(TranslationOptions):
    fields = ('voice_text', "third_text", "share_text")
translator.register(CloningAgreement, CloningAgreementTranslationsOption)

class PaymentRankTranslationsOption(TranslationOptions):
    fields = ("voicetime")
translator.register(PaymentRank, PaymentRankTranslationsOption)

