from django.urls import path
from register import views

urlpatterns  = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ko/google-login/', views.google_login, name='google-login'),  # 추가

]