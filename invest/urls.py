from django.urls import path
from invest import views

urlpatterns = [
    path("", views.invest_code, name='invest')

]