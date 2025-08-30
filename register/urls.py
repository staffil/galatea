from django.urls import path
from register import views

app_name = "register"
urlpatterns  = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),

]