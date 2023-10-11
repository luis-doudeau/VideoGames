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
    path('studio/', views.studio_listing, name='studios'),
    path('studio/form/', views.studioForm, name='studio_form'),
    path('edit-studio/<int:pk>/', views.StudioEditView.as_view(), name='edit_studio'),
    path('studio/<id>/', views.studio_detail, name='studio'),
    path('studio/<int:pk>/delete/', views.StudioDeleteView.as_view(), name='studio_delete'),
]
