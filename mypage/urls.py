from django.urls import path
from mypage import views

urlpatterns = [
    path('', views.mypage_view, name='mypage'),
    path('update/', views.mypage_update, name='mypage_update'),
    path('<int:user_id>/', views.mypage_update, name='mypage_update'),
    path('my_voice/', views.my_voice, name='my_voice'),
    path('my_ai_models/<int:llm_id>/', views.my_ai_models, name='my_ai_models'),
    path('upload-profile-image/', views.upload_profile_image, name='upload_profile_image'),
    path('my_ai_models/update/<int:llm_id>', views.my_ai_models_update, name='my_ai_models_update'),
    path('my_ai_models/delete/<int:llm_id>', views.my_ai_models_delete, name='my_ai_models_delete'),

]