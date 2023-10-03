from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('games/', views.game_listing, name='games'),
]
