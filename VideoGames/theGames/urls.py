from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('games/', views.GameListView.as_view(), name='games'),
    path('games/form/', views.GameCreateView.as_view(), name='game_form'),
    path('games/detail/<int:pk>/',
         views.GameDetailView.as_view(), name='game_detail'),


    path('games/<int:pk>/delete/',
         views.GameDeleteView.as_view(), name='game_delete'),
    path('games/<int:pk>/edit/', views.GameEditView.as_view(), name='edit_game'),

    path('studio/', views.StudioListView.as_view(), name='studios'),
    path('studio/form/', views.StudioCreateView.as_view(), name='studio_form'),
    path('studio/<int:pk>/', views.StudioDetailView.as_view(),
         name='studio_detail'),  # Utilisation de pk au lieu de id
    path('studio/<int:pk>/edit/', views.StudioEditView.as_view(), name='edit_studio'),
    path('studio/<int:pk>/delete/',
         views.StudioDeleteView.as_view(), name='studio_delete'),
    path('create_platform/', views.PlatformCreateView.as_view(),
         name='create_platform'),
]
