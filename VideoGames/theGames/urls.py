from django.urls import path
from . import views
from django.views import View

urlpatterns = [
    path('home/', views.home, name='home'),
    path('games/', views.game_listing, name='games'),
    path("games/form/", views.gameForm, name="game_form"),
    path('games/<id>/', views.game_detail, name='game'), # à mettre à la fin
    path('games/<int:pk>/delete/', views.GameDeleteView.as_view(), name='game_delete'),
    path('edit-game/<int:pk>/', views.GameEditView.as_view(), name='edit_game'),
]
