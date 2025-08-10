from django.urls import path
from celebrity import views
app_name = 'celebrity'

urlpatterns = [
    path("<int:celebrity_id>/", views.celebrity_view, name="celebrity_view"),

]