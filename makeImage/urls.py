from django.urls import path
from makeImage import views

urlpatterns = [
    path("", views.make_image_page, name="make_image_page"),
    path("image_app/", views.image_app, name="image_app"),
   
]