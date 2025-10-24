from django.urls import path, include
from customer_ai import views
from django.contrib.sitemaps.views import sitemap
from customer_ai.sitemaps import LLMSitemapAllModes
from rest_framework import routers
from customer_ai.views import VoiceListViewSet, LLMViewSet  # ViewSet 불러오기

# Sitemap
sitemaps = {
    'customer_ai': LLMSitemapAllModes(),
}

# REST API Router 생성
router = routers.DefaultRouter()
router.register(r'voice_list', VoiceListViewSet)
router.register(r'llm', LLMViewSet)

# URL Patterns
urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),

    path('upload_audio/', views.upload_audio, name='upload_audio'),
    path('generate_response/', views.generate_response, name='generate_response'),
    path('check_audio_status/', views.check_audio_status, name='check_audio_status'),

    path('chat/<int:llm_id>/', views.chat_view, name='chat_view'),
    path('vision/<int:llm_id>/', views.vision_view, name='vision_view'),
    path('novel/<int:llm_id>/', views.novel_view, name='novel_view'),

    path('make_ai/', views.make_ai, name='make_ai'),
    path('image-file/', views.is_allowed_image_file, name='image-file'),
    path('vision_process/', views.vision_process, name='vision_process'),
    path("ai_name/", views.input_ai_name, name="input_ai_name"),
    path('upload_image/', views.upload_image, name='upload_image'),

    # REST API 경로
    path('api/', include(router.urls)),
]
