from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views as home_views
from django.views.i18n import set_language
from django.utils.translation import get_language
from django.shortcuts import redirect
from celebrity import views as celebrity_views
from customer_ai import views as customer_ai_views
from makeImage import views as make_image_view

def root_redirect(request):
    lang = get_language()
    return redirect(f'/{lang}/')


urlpatterns = [
    path('', root_redirect),  # 루트 접속 시 언어별 URL로 리다이렉트
    path('accounts/', include('allauth.urls')), 
    path('admin/', admin.site.urls),
    path('i18n/setlang/', set_language, name='set_language'),

    path('celebrity/celebrity_audio/', celebrity_views.celebrity_audio, name='celebrity_audio'),
    path('celebrity/<int:celebrity_id>/response/', celebrity_views.celebrity_response, name='celebrity_response'),
    path('upload_audio/', customer_ai_views.upload_audio, name='upload_audio'),
    path('generate_response/', customer_ai_views.generate_response, name='generate_response'),
    path('vision_process/', customer_ai_views.vision_process, name='vision_process'),
    path("generate_image/", make_image_view.generate_image, name="generate_image"),
    path('proxy_image/', make_image_view.proxy_image, name='proxy_image'),  # 이미지 프록시용

]

urlpatterns += i18n_patterns(
    path('', include('home.urls', namespace='home')),  # home.urls 안에 main/ 포함
    path('celebrity/', include(('celebrity.urls', 'celebrity'), namespace='celebrity')),
    path('customer_ai/', include(('customer_ai.urls', 'customer_ai'), namespace='customer_ai')),
    path('image/', include(('makeImage.urls', 'makeImage'), namespace='makeImage')),
    path('make_voice/', include(('makeVoice.urls', 'makeVoice'), namespace='makeVoice')),
    path('register/', include(('register.urls', 'register'), namespace='register')),
    path('logout/', home_views.user_logout, name='logout'),
    path('mypage/', include(("mypage.urls","mypage"), namespace="mypage")),
    # path('cloning/', include(('cloning.urls', 'cloning'), namespace='cloning')),
    path('payment/', include(('payment.urls', 'payment'), namespace='payment'))
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
