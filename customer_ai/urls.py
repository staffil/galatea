from django.urls import path
from customer_ai import views


urlpatterns = [
    path('upload_audio/', views.upload_audio, name='upload_audio'),
    path('generate_response/', views.generate_response, name='generate_response'),

    path('chat/<int:llm_id>', views.chat_view, name='chat_view'),

    path('vision/<int:llm_id>/', views.vision_view, name='vision_view'),
    path('make_ai/', views.make_ai, name='make_ai'),

    path('image-file/', views.is_allowed_image_file, name='image-file'),
    path('vision_process/', views.vision_process, name='vision_process'),
    path("ai_name/", views.input_ai_name, name="input_ai_name"),
    # path('generate_image/<int:llm_id>/', views.generate_ai_image, name='generate_ai_image'),
    path('upload_image/', views.upload_image, name='upload_image'),



]
