from django.urls import path
from helpdesk import views

urlpatterns = [
    path('FAQ/', views.faq, name="Faq"),
    path('request/', views.request, name="request"),
    path('notice/', views.notice, name="notice"),
    path('notice_detail/<int:notice_id>/', views.notice_detail, name = 'notice_detail'),
    path("prompt_desk", views.prompt_share, name="prompt_share"),
    path("prompt_share_write/", views.prompt_share_write, name = 'prompt_share_write'),
    path("promtp_share_detail/<int:prompt_id>/", views.prompt_share_detail, name="prompt_share_detail"),
    path('prompt_share/<int:prompt_id>/delete/', views.prompt_share_delete, name='prompt_share_delete'),
    path('prompt_share/<int:prompt_id>/update/', views.prompt_share_update, name='prompt_share_update'),

    path("request/write", views.request_write, name='request_write'),
    path('request/detail<int:pk>/', views.request_detail, name='request_detail'),
    path("reuqest/<int:pk>/delete/", views.request_delete, name= 'request_delete')
]