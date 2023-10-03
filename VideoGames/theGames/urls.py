from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('games/', views.game_listing, name='games'),
    path('games/<id>', views.game_detail, name='game'),
    path("games/form", views.gameForm, name="game_form")

]
