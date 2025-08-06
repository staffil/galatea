from django.urls import path
from supertone import views

urlpatterns = [
    path("", views.supertone_experiment, name='supertone')
]
