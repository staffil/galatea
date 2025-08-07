"""
URL configuration for galatea project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views 
from django.contrib.auth.views import LogoutView
from home import views as home_views
urlpatterns = [
    path("admin/", admin.site.urls),
# project/urls.py
    path('celebrity/', include(('celebrity.urls', 'celebrity'), namespace='celebrity')),
    path('customer_ai/', include(('customer_ai.urls', 'customer_ai'), namespace='customer_ai')),
    path('image/', include(('makeImage.urls', 'makeImage'), namespace='makeImage')),
    path('', include(('home.urls', 'home'), namespace='home')),
    path('main/', views.main, name='main'),
    path('make_voice/', include(('makeVoice.urls', 'makeVoice'), namespace='makeVoice')),
    path('register/', include(('register.urls', 'register'), namespace='register')),
    path('logout/', home_views.user_logout, name='logout'),  
    path('mypage/', include(("mypage.urls","mypage"),namespace="mypage")),
    # path('payment/', include(('payment.urls', 'payment'), namespace='payment')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
