from django.urls import path
from . import views

urlpatterns = [
    path('', views.News_Articles),
]