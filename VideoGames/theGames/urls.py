from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('games/', views.game_listing, name='games'),
    path("games/form/", views.gameForm, name="game_form"),
    path('games/<id>/', views.game_detail, name='game'), # à mettre à la fin 
    path('games/<int:id>/', views.my_task_delete, name='delete_object'), 
]
