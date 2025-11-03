from django.urls import path
from distribute import views

app_name = 'distribute'

urlpatterns =[
    path('<int:llm_id>/', views.distribute, name='distribute'),
    path('<int:llm_id>/unpublic/', views.unpublish_llm, name= 'unpublic'),



    path('distribute_app/<int:llm_id>/', views.distribute_app, name= 'distribute_app'),

    path('<int:llm_id>/unpublish_llm_app/', views.unpublish_llm_app, name= 'unpublish_llm_app'),


]