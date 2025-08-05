from django.urls import path
from makeImage import views

urlpatterns = [
    path("", views.make_image_page, name="make_image_page"),
    path("generate_image/", views.generate_image, name="generate_image"),
    path('proxy_image/', views.proxy_image, name='proxy_image'),  # 이미지 프록시용

]