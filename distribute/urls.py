from django.urls import path
from distribute import views

app_name = 'distribute'

urlpatterns =[
    path('<int:llm_id>/', views.distribute, name='distribute'),
    path('<int:llm_id>/unpublic/', views.unpublish_llm, name= 'unpublic'),

]