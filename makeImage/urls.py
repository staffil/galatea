from django.urls import path
from makeImage import views

urlpatterns = [
    path("", views.make_image_page, name="make_image_page"),
   
]