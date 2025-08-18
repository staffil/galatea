from django.urls import path
from helpdesk import views

urlpatterns = [
    path('FAQ/', views.faq, name="Faq"),
    path('notice/', views.notice, name="notice"),
    path('request/', views.request, name="request"),
    path("request/write", views.request_write, name='request_write'),
    path('request/detail<int:pk>/', views.request_detail, name='request_detail')
   
]