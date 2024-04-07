from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('banner', views.banner_view),
    path('banner/<int:banner_id>', views.update_banner),
]
