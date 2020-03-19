from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('visited', views.visited, name='visited'),
    path('place/<int:place_pk>/was_visited/', views.place_was_visited, name='place_was_visited')
]