from django.urls import path
from helpdesk import views

urlpatterns = [
    path('FAQ/', views.faq, name="Faq"),
    path('request/', views.request, name="request"),
    path('notice/', views.notice, name="notice"),
    path('notice_detail/<int:notice_id>/', views.notice_detail, name = 'notice_detail'),
    path("prompt_desk/", views.prompt_share, name="prompt_share"),
    path("prompt_share_write/", views.prompt_share_write, name = 'prompt_share_write'),
    path("promtp_share_detail/<int:prompt_id>/", views.prompt_share_detail, name="prompt_share_detail"),
    path('prompt_share/<int:prompt_id>/delete/', views.prompt_share_delete, name='prompt_share_delete'),
    path('prompt_share/<int:prompt_id>/update/', views.prompt_share_update, name='prompt_share_update'),

    path("request/write", views.request_write, name='request_write'),
    path('request/detail<int:pk>/', views.request_detail, name='request_detail'),
    path("reuqest/<int:pk>/delete/", views.request_delete, name= 'request_delete'),




    path("faq_app/", views.faq_app, name= 'faq_app'),
    path("request_app/", views.request_app, name= 'request_app'),
    path("request_write_app/", views.request_write_app, name= 'request_write_app'),
    path('request/detail_app<int:pk>/', views.request_detail_app, name='request_detail_app'),
    path("reuqest/<int:pk>/delete_app/", views.request_delete_app, name= 'request_delete_app'),
    path("notice_app/", views.notice_app, name= 'notice_app'),
    path('notice_detail_app/<int:notice_id>/', views.notice_detail_app, name = 'notice_detail_app'),
    path("prompt_share_app/", views.prompt_share_app, name= 'prompt_share_app'),
    path("prompt_share_write_app/", views.prompt_share_write_app, name= 'prompt_share_write_app'),
    path("prompt_share_detail_app/<int:prompt_id>/", views.prompt_share_detail_app, name="prompt_share_detail_app"),
    path('prompt_share/<int:prompt_id>/delete_app/', views.prompt_share_delete_app, name='prompt_share_delete_app'),
    path('prompt_share/<int:prompt_id>/update_app/', views.prompt_share_update_app, name='prompt_share_update_app'),



    
]