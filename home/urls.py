from django.urls import path
from home import views
from django.views.i18n import set_language

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),  
    path('main/', views.main, name='main'),
    path('logout/', views.user_logout, name='logout'),
    path('i18n/setlang/', set_language, name='set_language'),
    path('follow/', views.follow_toggle, name = "toggle_follow"),
    path('like/', views.like_toggle, name = 'like_toggle'),
    path('llm/<int:llm_id>/', views.llm_intro, name='llm_intro'),
    path('genres/', views.gerne_all, name= 'genre_all'),
    path('search/', views.search_llm, name = 'search_llm'),
    path('genres/<int:genres_id>', views.genre_detail, name='genres_detail'),
    path('llm_sections/', views.llm_section, name='llm_section'),
    path('comment_create/<int:llm_id>', views.comment_create, name="comment_create"),

    path("voice_all/", views.voice_all, name="voice_all"),
    path("save_voice/", views.save_voice, name="save_voice"),
    path("user_intro/<int:user_id>/", views.user_intro, name="user_intro"),
    path("soon/", views.soon, name="soon"),
    path('invite/', views.invite, name='invite'),


    # path('like/<int:llm_id>/', views.like_toggle, name = "like_toggle"),


    # 앱 전용
    path("app/", views.home_app_view, name="home_app"),
    path("main_app/", views.main_app, name="main_app"),
    path("llm_intro_app/<int:llm_id>/", views.llm_intro_app, name="llm_intro_app"),
    path("llm_section_app/", views.llm_section_app, name="llm_section_app"),

]

