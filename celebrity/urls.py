from django.urls import path
from celebrity import view

urlpatterns = [
    path("<int:celebrity_id>/", view.celebrity_view, name="celebrity_view"),
    path('celebrity_audio/', view.celebrity_audio, name='celebrity_audio'),
    path('celebrity_response/<int:celebrity_id>/', view.celebrity_response, name='celebrity_response'),
]