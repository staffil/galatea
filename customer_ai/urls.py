from django.urls import path
from customer_ai import views
from django.contrib.sitemaps.views import sitemap
from customer_ai.sitemaps import LLMSitemapAllModes

sitemaps = {
    'customer_ai': LLMSitemapAllModes(),
}

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]


urlpatterns = [
    path('upload_audio/', views.upload_audio, name='upload_audio'),
    path('generate_response/', views.generate_response, name='generate_response'),
    path('padcast_chat/', views.padcast_chat, name='padcast_chat'),

    path('chat/<int:llm_id>/', views.chat_view, name='chat_view'),

    path('vision/<int:llm_id>/', views.vision_view, name='vision_view'),
    path('novel/<int:llm_id>/', views.novel_view, name ='novel_view'),
    path('padcast/<int:llm_id>/', views.padcast_view, name ='padcast_view'),
    path('make_ai/', views.make_ai, name='make_ai'),

    path('image-file/', views.is_allowed_image_file, name='image-file'),
    path('vision_process/', views.vision_process, name='vision_process'),
    path("ai_name/", views.input_ai_name, name="input_ai_name"),
    # path('generate_image/<int:llm_id>/', views.generate_ai_image, name='generate_ai_image'),
    path('upload_image/', views.upload_image, name='upload_image'),



]
