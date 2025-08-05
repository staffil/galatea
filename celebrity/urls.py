from django.urls import path
from celebrity import views

urlpatterns = [
    path("<int:celebrity_id>/", views.celebrity_view, name="celebrity_view"),
    path('celebrity_audio/', views.celebrity_audio, name='celebrity_audio'),
    path('<int:celebrity_id>/response/', views.celebrity_response, name='celebrity_response'),
]