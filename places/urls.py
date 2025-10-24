from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('places/<int:pk>/', views.place_detail, name='place-detail'),
]