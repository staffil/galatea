from django.urls import path
from register import views

urlpatterns  = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('google-login/', views.google_login, name='google-login'),

]