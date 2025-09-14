from django.contrib import admin
from django.contrib.auth import get_user_model
from makeVoice.models import VoiceList
from user_auth.models import Authority, News
from customer_ai.models import Conversation, LLM
from celebrity.models import Celebrity,CelebrityVoice
from distribute.models import Genre
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user_auth.models import Faq, Requests, Notice, Gift
from cloning.models import CloningAgreement

User = get_user_model()


class ConversationInline(admin.TabularInline):
    model= Conversation
    extra=0
    readonly_fields= ('created_at',)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Users  # 실제 모델 이름

# 이미 등록되어 있으면 제거
try:
    admin.site.unregister(Users)
except admin.sites.NotRegistered:
    pass

# 기존 이름 그대로 UserAdmin 사용
@admin.register(Users)
class UserAdmin(BaseUserAdmin):
    list_display = ('사용자_번호', '사용자_아이디', '이메일_주소', '닉네임','보이스 이름', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'status')

    # 컬럼 이름 한글화
    @admin.display(description='사용자 번호')
    def 사용자_번호(self, obj):
        return obj.id

    @admin.display(description='사용자 아이디')
    def 사용자_아이디(self, obj):
        return obj.username

    @admin.display(description='이메일 주소')
    def 이메일_주소(self, obj):
        return obj.email
    
    @admin.display(description='닉네임')
    def 닉네임(self, obj):
        return obj.nickname
    
    @admin.display(description='보이스 이름')
    def 보이스_이름(self, obj):
        return obj.voice.name

    # inlines 설정
    inlines = [ConversationInline]  # ConversationInline 정의 필요

    # Users 모델 필드 기준으로 fieldsets 커스터마이즈
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('권한', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('프로필', {'fields': ('nickname', 'phonenumber', 'user_image', 'status', 'followers')}),
        ('로그인 정보', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)


class LLMConversationInline(admin.TabularInline):
    model = Conversation
    fk_name = 'llm'  # 추가
    extra = 0
    fields = ('created_at', 'user', 'user_message', 'llm_response',)
    readonly_fields = ('created_at', 'user', 'user_message', 'llm_response',)

@admin.register(LLM)
class LLMAdmin(admin.ModelAdmin):
    # list_display에는 정의한 @admin.display 메서드들의 이름이 들어가야 합니다.
    # 만약 커스텀 메서드를 사용한다면 그 메서드 이름을 여기에 넣어주세요.
    # 예를 들어, 메서드 이름을 'get_id_display' 등으로 명확히 하는 것이 좋습니다.
    list_display= ('get_id_display', 'get_name_display', 'get_created_at_display', 'get_update_at_display') # <-- 수정된 부분

    search_fields = ('name', 'prompt',) # LLM 모델의 필드이므로 'name', 'prompt'로 접근하는 것이 맞습니다.

    # === 아래 @admin.display 메서드들을 수정합니다. ===
    @admin.display(description="LLM 번호")
    def get_id_display(self, obj): # 메서드 이름 변경 권장: 'id'는 필드 이름과 겹쳐 혼동 가능
        return obj.id # obj는 LLM 인스턴스이므로 obj.id로 직접 접근

    @admin.display(description="LLM 이름")
    def get_name_display(self, obj): # 메서드 이름 변경 권장
        return obj.name # obj는 LLM 인스턴스이므로 obj.name으로 직접 접근

    @admin.display(description="생성날짜")
    def get_created_at_display(self, obj): # 메서드 이름 변경 권장
        return obj.created_at # obj는 LLM 인스턴스이므로 obj.created_at으로 직접 접근

    @admin.display(description="수정날짜")
    def get_update_at_display(self, obj): # 메서드 이름 변경 권장
        return obj.update_at # obj는 LLM 인스턴스이므로 obj.update_at으로 직접 접근
    # =================================================

    inlines = [LLMConversationInline]


@admin.register(VoiceList)
class VoiceListAdmin(admin.ModelAdmin): 
    list_display=("get_user_id_display", "get_user_username_display", "get_voice_id_display", "get_voice_name_display", ) # 메서드 이름으로 변경

    @admin.display(description="사용자 번호") # 컬럼 헤더 이름
    def get_user_id_display(self, obj): # 메서드 이름
        return obj.user.id if obj.user else None 

    @admin.display(description='사용자 이름') # 컬럼 헤더 이름 (사용자 아이디가 아니라 '이름'으로 가정)
    def get_user_username_display(self, obj): # 메서드 이름
        return obj.user.username if obj.user else 'N/A' # VoiceList의 user 필드에서 username을 가져옴.

    @admin.display(description="목소리 ID") # 컬럼 헤더 이름
    def get_voice_id_display(self, obj): # 메서드 이름
        return obj.voice_id # VoiceList 모델에 voice_id 필드가 있다고 가정

    @admin.display(description="목소리 이름") # 컬럼 헤더 이름
    def get_voice_name_display(self, obj): # 메서드 이름
        # VoiceList 모델에 'voice_name' 필드가 있다고 가정합니다.
        # 만약 'Voice' 모델에 이름이 있고, VoiceList가 Voice를 ForeignKey로 참조한다면
        # return obj.voice.name if obj.voice else None
        # 현재 VoiceList 모델에 voice_name 필드가 없으면 오류가 발생합니다.
        # VoiceList 모델에 직접 'name' 필드나 Voice 모델의 'name' 필드를 참조하는 방식이 필요합니다.
        return obj.voice_name # 'voice_name' 필드가 VoiceList 모델에 있다고 가정


    # list_filter와 search_fields는 VoiceList 모델의 실제 필드를 참조해야 합니다.
    # VoiceList 모델에 'user' 필드가 ForeignKey로 연결되어 있다면 'user'로 필터링 가능
    list_filter = ('user',)
    # 검색 필드도 VoiceList 모델의 실제 필드를 참조
    # user__username (user 모델의 username), voice_id, voice_name (만약 있다면)
    search_fields = ('user__username', 'voice_id', 'voice_name',)
    


from django.contrib.admin import DateFieldListFilter
from django.utils.timezone import localtime
from datetime import date

class CreatedAtDayFilter(admin.SimpleListFilter):
    title = '생성일'
    parameter_name = 'created_day'

    def lookups(self, request, model_admin):
        days = model_admin.model.objects.dates('created_at', 'day', order='DESC')
        return [(d.strftime("%Y-%m-%d"), d.strftime("%Y-%m-%d")) for d in days]

    def queryset(self, request, queryset):
        if self.value():
            day = date.fromisoformat(self.value())
            return queryset.filter(created_at__date=day)
        return queryset


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('get_id_display', 'get_llm_display', 'get_user_display', 'get_created_at_display', 'get_user_message_display')
    list_filter = (
        ('created_at', DateFieldListFilter),
        'user',
        'llm',
    )
    search_fields = ('user__username', 'llm__name', 'user_message', 'llm_response')
    
    @admin.display(description="id")
    def get_id_display(self, obj):
        return obj.id
    
    @admin.display(description="LLM 이름")
    def get_llm_display(self, obj):
        return obj.llm.name
    
    @admin.display(description="사용자 이름")
    def get_user_display(self, obj):
        return obj.user.username
    
    @admin.display(description="생성날짜")
    def get_created_at_display(self, obj):
        return obj.created_at
    
    @admin.display(description="사용자 메시지")
    def get_user_message_display(self, obj):
        return obj.user_message
    
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'llm', 'created_at', 'user_message', 'llm_response')
        }),
    )









@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    list_display = ('get_celebrity_name_display', 'get_description_display') # 목록에 표시할 필드
    search_fields = ('celebrity_name', 'celebrity_prompt') # 검색 기능에 사용할 필드
    list_filter = ('celebrity_voice_id',) # 사이드바에 필터로 사용할 필드

    @admin.display(description="celebrity 이름")
    def get_celebrity_name_display(self, obj):
        return obj.celebrity_name
    
    @admin.display(description="설명")
    def get_description_display(self, obj):
        return obj.description


@admin.register(CelebrityVoice)
class CelebrityVoiceAdmin(admin.ModelAdmin):
    list_display = ("get_celebrity_voice_name", 'get_sample_url', 'get_celebrity_voice_id')    
    search_fields = ('name','sample_url', 'celebrity_voice_id')
    list_filter= ('name',)

    @admin.display(description="celebrity_voice 이름")
    def get_celebrity_voice_name(self, obj):
        return obj.name
    
    @admin.display(description="celebrity_voice 샘플")
    def get_sample_url(self, obj):
        return obj.sample_url
    @admin.display(description="celebrity_voice_id")
    def get_celebrity_voice_id(self, obj):
        return obj.celebrity_voice_id


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("get_genre_name", "get_genre_img")

    @admin.display(description='genre 이름')
    def get_genre_name(self, obj):
        return obj.name  # 'name' 필드로 수정

    @admin.display(description="genre 이미지")
    def get_genre_img(self, obj):
        if obj.genre_image:
            return obj.genre_image.url  # 이미지 URL 반환
        return "-"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display= ("get_title", "get_news_img", "get_news_description", "get_link")

    @admin.display(description="뉴스 타이틀")
    def get_title(self, obj):
        if obj.title:
            return obj.title
        
    @admin.display(description="뉴스 이미지")
    def get_news_img(self, obj):
        if obj.news_img:
            return obj.news_img
        
    @admin.display(description="뉴스 설명")
    def get_news_description(self, obj):
        if obj.news_description:
            return obj.news_description
        
    @admin.display(description="링크")
    def get_link(self, obj):
        if obj.link:
            return obj.link

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display= ("get_title", 'get_content', 'get_faq_img')

    @admin.display(description="faq 제목")
    def get_title(self, obj):
        if obj.title:
            return obj.title
        
    @admin.display(description="faq 내용")
    def get_content(self, obj):
        if obj.content:
            return obj.content
        
    @admin.display(description="faq 이미지")
    def get_faq_img(self, obj):
        if obj.faq_img:
            return obj.faq_img
        

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("get_title", "get_content", "get_author")  

    @admin.display(description="공지사항 제목")
    def get_title(self, obj):
        return obj.title if obj.title else "-"
        
    @admin.display(description="공지사항 내용")
    def get_content(self, obj):
        return obj.content if obj.content else "-"
        
    @admin.display(description="올린 관리자")
    def get_author(self, obj):
        return obj.author.username if obj.author else "-"
    

@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ("get_title", "get_gift_img", )

    @admin.display(description="이벤트 제목")
    def get_title(self, obj):
        return obj.title
    
    @admin.display(description="이벤트 사진")
    def get_gift_img(self, obj):
        return obj.gift_img
    
    
        
from django.contrib import admin
from payment.models import (
    PaymentMethod,
    PaymentRank,
    Payment,
    Token,
    TokenHistory,
    TotalToken,
    PaymentStats,
)

# 결제 수단
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('name',)

# 결제 등급
@admin.register(PaymentRank)
class PaymentRankAdmin(admin.ModelAdmin):
    list_display = ('rankname', 'price', 'voicetime', 'freetoken', 'color',)
    search_fields = ('rankname',)

# 결제 내역
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_rank', 'amount', 'status', 'paid_at', 'payment_method', 'imp_uid', 'merchant_uid')
    list_filter = ('status', 'payment_method', 'payment_rank')
    search_fields = ('user__username', 'imp_uid', 'merchant_uid')

# 토큰
@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_token', 'token_usage', 'created_at')
    search_fields = ('user__username',)

# 토큰 히스토리
@admin.register(TokenHistory)
class TokenHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'change_type', 'amount', 'total_voice_generated', 'created_at')
    list_filter = ('change_type',)
    search_fields = ('user__username',)

# 총 토큰
@admin.register(TotalToken)
class TotalTokenAdmin(admin.ModelAdmin):
    list_display = ('total_tokens_used', 'total_llm_count', 'updated_at')

# 결제 통계
@admin.register(PaymentStats)
class PaymentStatsAdmin(admin.ModelAdmin):
    list_display = ('total_payments', 'success_count', 'failure_count', 'pending_count', 'refunded_count', 'updated_at')


@admin.register(CloningAgreement)
class CloningAgreementAdmin(admin.ModelAdmin):
    list_display = ('voice_text', 'third_text', 'share_text')

