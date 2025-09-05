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
from register import views as login_view
from home import views as main_view
from makeVoice import views as make_voice_view
from helpdesk import views as helpdesk_view
from payment import views as payment_view
from django.contrib.sitemaps.views import sitemap
from home.sitemaps import StaticViewSitemap

def root_redirect(request):
    lang = get_language()
    return redirect(f'/{lang}/')

sitemaps = {
    "static": StaticViewSitemap,
}
urlpatterns = [
    path('', root_redirect),  # 루트 접속 시 언어별 URL로 리다이렉트
    path('admin/', admin.site.urls),
    path('i18n/setlang/', set_language, name='set_language'),
    path('accounts/', include('allauth.urls')), 

    path('celebrity/celebrity_audio/', celebrity_views.celebrity_audio, name='celebrity_audio'),
    path('celebrity/<int:celebrity_id>/response/', celebrity_views.celebrity_response, name='celebrity_response'),
    path('upload_audio/', customer_ai_views.upload_audio, name='upload_audio'),
    path('generate_response/', customer_ai_views.generate_response, name='generate_response'),
    path('vision_process/', customer_ai_views.vision_process, name='vision_process'),
    path('novel_process/', customer_ai_views.novel_process, name = "novel_process"),

    path("generate_image/", make_image_view.generate_image, name="generate_image"),
    path('proxy_image/', make_image_view.proxy_image, name='proxy_image'),  # 이미지 프록시용
    path('<int:llm_id>/introduce', main_view.distribute_llm, name='distribute_llm'),
    path("auto_generate_prompt", make_voice_view.auto_generate_prompt, name="auto_generate_prompt") ,           
    path("auto_prompt/", customer_ai_views.auto_prompt, name="auto_prompt"),
    path("payment/complete/", payment_view.payment_complete, name="payment_complete"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),



]

urlpatterns += i18n_patterns(
    
    path('', include('home.urls', namespace='home')),  # home.urls 안에 main/ 포함
    path('celebrity/', include(('celebrity.urls', 'celebrity'), namespace='celebrity')),
    path('customer_ai/', include(('customer_ai.urls', 'customer_ai'), namespace='customer_ai')),
    path('image/', include(('makeImage.urls', 'makeImage'), namespace='makeImage')),
    # path('make_voice/', include(('makeVoice.urls', 'makeVoice'), namespace='makeVoice')),
    path('register/', include(('register.urls', 'register'), namespace='register')),
    path('logout/', home_views.user_logout, name='logout'),
    path('mypage/', include(("mypage.urls","mypage"), namespace="mypage")),
    # path('cloning/', include(('cloning.urls', 'cloning'), namespace='cloning')),
    path('payment/', include(('payment.urls', 'payment'), namespace='payment')),
    path("distribute/", include(("distribute.urls", 'distribute'), namespace="distribute")),
    path('intro/<int:llm_id>/', main_view.llm_detail_partial, name='llm_detail_partial'),
    path('helpdesk/', include(("helpdesk.urls", 'helpdesk'), namespace='helpdesk')),
    path('invest/', include(("invest.urls", 'invest'), namespace='invest')),
    path('login/', include('social_django.urls', namespace='login')),





)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
