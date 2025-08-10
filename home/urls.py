from django.urls import path
from home import views
from django.views.i18n import set_language

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),  
    path('main/', views.main, name='main'),
    path('logout/', views.user_logout, name='logout'),
    path('i18n/setlang/', set_language, name='set_language'),
]
