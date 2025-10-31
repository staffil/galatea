from django.urls import path
from register import views

app_name = "register"
urlpatterns  = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),

    path('auth/google/callback/', views.google_callback, name='google_callback'),  


    path('login_app/', views.login_app, name='login_app'),
    path('signup_app/', views.signup_app, name='signup_app'),
]