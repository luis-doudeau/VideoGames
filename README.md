# Projet Django de Gestion de Jeux Vidéo

Ce projet Django est une application web pour gérer une collection de jeux vidéo, les studios qui les ont créés, ainsi que les plateformes sur lesquelles les jeux sont disponibles.
Fonctionnalités principales

    Liste des jeux vidéo disponibles.
    Création, mise à jour, visualisation, et suppression de jeux vidéo.
    Liste des studios de jeux vidéo.
    Création, mise à jour, visualisation, et suppression de studios.
    Création de nouvelles plateformes de jeux vidéo.

## Dépendances

    Python
    Django
    FuzzyWuzzy (pour la comparaison de similarité de chaînes)

## Installation

    Clonez ce dépôt dans votre environnement local.
    Naviguez jusqu'au dossier du projet dans votre terminal.
    Exécutez pip install -r requirements.txt pour installer les dépendances nécessaires.
    Lancez le serveur de développement Django en utilisant python manage.py runserver.
    Ouvrez votre navigateur web et accédez à http://127.0.0.1:8000/.

## Utilisation
### Jeux vidéo

    Accédez à /home/ pour voir le message d'accueil.
    Accédez à /games/ pour voir la liste des jeux vidéo.
    Accédez à /games/form/ pour créer un nouveau jeu vidéo.
    Accédez à /games/detail/{game_id}/ pour voir les détails d'un jeu vidéo spécifique.
    Accédez à /games/{game_id}/edit/ pour modifier un jeu vidéo.
    Accédez à /games/{game_id}/delete/ pour supprimer un jeu vidéo.

### Studios

    Accédez à /studio/ pour voir la liste des studios.
    Accédez à /studio/form/ pour créer un nouveau studio.
    Accédez à /studio/{studio_id}/ pour voir les détails d'un studio spécifique.
    Accédez à /studio/{studio_id}/edit/ pour modifier un studio.
    Accédez à /studio/{studio_id}/delete/ pour supprimer un studio.

### Plateformes

    Accédez à /create_platform/ pour créer une nouvelle plateforme de jeu.

## Modèles

    Game : Contient des informations sur les jeux vidéo, y compris le nom, la description, le studio, et les plateformes.
    Studio : Contient des informations sur les studios, y compris le nom, la description, et le pays.
    Platform : Contient des informations sur les plateformes de jeu, y compris le nom, la description, et le fabricant.

## Vues

Le projet utilise des vues basées sur des classes (Class-Based Views) pour différentes fonctionnalités, telles que ListView, DetailView, CreateView, DeleteView, et UpdateView. Ces vues sont utilisées pour gérer les jeux, les studios, et les plateformes.
Formulaires

    GameForm : Pour créer ou modifier des jeux vidéo. Contient de la logique pour gérer la création de nouvelles plateformes si elles n'existent pas déjà.
    StudioForm : Pour créer ou modifier des studios de jeux vidéo.
    PlatformForm : Pour créer de nouvelles plateformes de jeux vidéo.

## Validation

La validation est gérée dans les méthodes form_valid de chaque vue. Par exemple, GameCreateView vérifie si un jeu avec un nom similaire ou identique existe déjà avant de permettre la création d'un nouveau jeu.

## Pagination

La pagination est implémentée dans GameListView et StudioListView avec une limite de 6 éléments par page.