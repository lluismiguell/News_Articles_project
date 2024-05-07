from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('categories', views.getCats),
    path('authors', views.getAuthors),
]