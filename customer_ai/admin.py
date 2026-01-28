from django.contrib import admin
from .models import LLM, LLMSubImage, Conversation, LlmLike, Prompt


# LLM 서브 이미지 인라인 (LLM 편집 시 함께 편집 가능)
class LLMSubImageInline(admin.TabularInline):
    model = LLMSubImage
    extra = 1  # 빈 폼 1개 표시
    fields = ['image', 'title', 'description', 'order']
    ordering = ['order']


@admin.register(LLM)
class LLMAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'is_public', 'llm_like_count', 'created_at']
    list_filter = ['is_public', 'model', 'created_at']
    search_fields = ['name', 'user__username', 'user__email']
    inlines = [LLMSubImageInline]  # LLM 편집 화면에서 서브 이미지 추가 가능


@admin.register(LLMSubImage)
class LLMSubImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'llm', 'title', 'order', 'created_at']
    list_filter = ['llm', 'created_at']
    search_fields = ['llm__name', 'title']
    ordering = ['llm', 'order']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'llm', 'created_at']
    list_filter = ['llm', 'created_at']
    search_fields = ['user__username', 'user__email']


@admin.register(LlmLike)
class LlmLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'llm', 'is_like', 'created_at']
    list_filter = ['is_like', 'created_at']


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'prompt_title', 'prompt_type', 'created_at']
    list_filter = ['prompt_type', 'created_at']
    search_fields = ['prompt_title', 'user__username']
