from django.urls import path
from mypage import views

app_name = 'mypage'

urlpatterns = [
    path('', views.mypage_view, name='mypage'),
    path('update/', views.mypage_update, name='mypage_update'),
    path('<int:user_id>/', views.mypage_update, name='mypage_update'),
    path('my_voice/', views.my_voice, name='my_voice'),
    path('my_ai_models/<int:llm_id>/', views.my_ai_models, name='my_ai_models'),
    path('my_ai_conversation/<int:llm_id>/', views.my_ai_conversation, name="my_ai_conversation"),
    path('token/', views.personal_token, name = 'token'),
    path('upload-profile-image/', views.upload_profile_image, name='upload_profile_image'),
    path('my_ai_models/update/<int:llm_id>', views.my_ai_models_update, name='my_ai_models_update'),
    path('my_ai_models/delete/<int:llm_id>', views.my_ai_models_delete, name='my_ai_models_delete'),
    # path('<int:voice_id>/toggle_public/', views.toggle_voice_public, name='toggle_voice_public'),
    path("my_custom/", views.my_custom, name= "my_custom"),
    path("my_request/", views.my_request, name= "my_request"),
    path("my_coupon/", views.my_coupon, name= "my_coupon"),
    path("myvoice/delete/<int:voice_id>/", views.my_voice_delete, name="my_voice_delete"),
    path('personal_profile/', views.personal_profile, name="personal_profile"),
    path('llm_like/', views.llm_like, name="llm_like"),
    path('follow_list/', views.follow_list, name="follow_list"),
    path("unpublish_llm/<int:llm_id>/", views.unpublish_llm, name="unpublish_llm"),
    path('prompt_share/<int:prompt_id>/delete/', views.prompt_share_delete, name='prompt_share_delete'),
    path('prompt_share/<int:prompt_id>/update/', views.prompt_share_update, name='prompt_share_update'),
    path('intro/<int:llm_id>/', views.llm_intro, name='llm_intro'),
    path('token_less/', views.token_less, name='token_less'),
    

    path("mypage_app/", views.mypage_app, name="mypage_app"),
    path('sidebar_app/', views.sidebar_app, name='sidebar_app'),
    path('mypage_update_app/', views.mypage_update_app, name='mypage_update_app'),
    path('my_ai_models_app/<int:llm_id>/', views.my_ai_models_app, name='my_ai_models_app'),
    path('my_ai_conversation_app/<int:llm_id>', views.my_ai_conversation_app, name='my_ai_conversation_app'),
    path('my_voice_app/', views.my_voice_app, name='my_voice_app'),
    path('my_voice_delete_app/', views.my_voice_delete_app, name='my_voice_delete_app'),
    path('my_ai_models_update_app/<int:llm_id>/', views.my_ai_models_update_app, name='my_ai_models_update_app'),
    path('follow_list_app/', views.follow_list_app, name='follow_list_app'),
    path('my_coupon_app/', views.my_coupon_app, name='my_coupon_app'),
    path('token_less_app/', views.token_less_app, name='token_less_app'),
    path('personal_profile_app/', views.personal_profile_app, name='personal_profile_app'),
    path('my_request_app/', views.my_request_app, name='my_request_app'),
    path('llm_like_app/', views.llm_like_app, name='llm_like_app'),
    path('token_app/', views.token_app, name='token_app'),
    path('unpublish_llm_app/<int:llm_id>/', views.unpublish_llm_app, name='unpublish_llm_app'),
    path('my_ai_models/delete_app/<int:llm_id>', views.my_ai_models_delete_app, name='my_ai_models_delete_app'),


]