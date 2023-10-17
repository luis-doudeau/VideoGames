from django.test import TestCase
from django.urls import reverse
from .models import Game, Studio, Platform
from django.db import IntegrityError


class GameTests(TestCase):

    def setUp(self):
        # Créer des studios
        self.test_studio = Studio.objects.create(
            name="Test Studio",
            description="Ceci est un studio de test",
            country="US"
        )

        self.another_test_studio = Studio.objects.create(
            name="Another Test Studio",
            description="Ceci est un autre studio de test",
            country="US"
        )

        # Créer des plateformes
        self.platform1 = Platform.objects.create(
            name="Test Platform 1",
            description="Ceci est une plateforme de test",
            manufacturer="Fabricant de Test 1"
        )

        self.platform2 = Platform.objects.create(
            name="Test Platform 2",
            description="Ceci est une autre plateforme de test",
            manufacturer="Fabricant de Test 2"
        )

        # Créer des jeux avec les studios
        self.game1 = Game.objects.create(
            name="Test Game 1",
            description="Ceci est un jeu de test",
            studio=self.test_studio
        )
        # Ajouter une plateforme au jeu
        self.game1.platforms.add(self.platform1)

        self.game2 = Game.objects.create(
            name="Test Game 2",
            description="Ceci est un autre jeu de test",
            studio=self.another_test_studio
        )
        # Ajouter une plateforme au jeu
        self.game2.platforms.add(self.platform2)

    # Test pour la vue de liste des jeux
    def test_game_listing_view(self):
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game 1')
        self.assertContains(response, 'Test Game 2')

    # Test pour la vue de détail d'un jeu valide
    def test_game_detail_view_valid_game(self):
        response = self.client.get(
            reverse('game_detail', args=[self.game1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game 1')

    # Test pour la vue de détail d'un jeu non valide
    def test_game_detail_view_invalid_game(self):
        response = self.client.get(reverse('game_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    # Test pour obtenir la vue du formulaire de jeu
    def test_game_form_view_get(self):
        response = self.client.get(reverse('game_form'))
        self.assertEqual(response.status_code, 200)
        # Vérification de la présence d'une balise de formulaire
        self.assertContains(response, '<form')

    # Test pour poster dans la vue du formulaire de jeu
    def test_game_form_view_post(self):
        donnees_post = {
            'name': 'Test Game 3',
            'description': 'Un troisième jeu de test.',
            'studio': self.test_studio.id,
            'platforms': [self.platform1.id],
            'confirm': 'true'  # simuler la confirmation de l'utilisateur
        }
        response = self.client.post(
            reverse('edit_game', args=[self.game1.id]), donnees_post)
        self.assertEqual(response.status_code, 302)
        # Récupération de la nouvelle instance de jeu
        new_game = Game.objects.filter(name='Test Game 3').first()
        self.assertIsNotNone(new_game)  # Assurez-vous que le jeu a été créé
        self.assertTrue(new_game.platforms.filter(
            id=self.platform1.id).exists())  # Vérification de l'association de la plateforme

    # Test pour obtenir la vue de suppression de jeu
    def test_game_delete_view_get(self):
        response = self.client.get(
            reverse('game_delete', args=[self.game1.id]))
        self.assertEqual(response.status_code, 200)

    # Test pour poster dans la vue de suppression de jeu
    def test_game_delete_view_post(self):
        response = self.client.post(
            reverse('game_delete', args=[self.game1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Game.objects.filter(id=self.game1.id).exists())

    # Test pour obtenir la vue d'édition de jeu
    def test_game_edit_view_get(self):
        response = self.client.get(reverse('edit_game', args=[self.game1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game 1')

    # Test pour poster dans la vue d'édition de jeu
    def test_game_edit_view_post(self):
        # Simuler que l'utilisateur a confirmé la modification
        donnees_post = {
            'name': 'Jeu Test Mis à Jour 1',
            'description': 'Description mise à jour.',
            'studio': self.test_studio.id,
            'platforms': [self.platform1.id],
            'confirm': 'true'  # simuler la confirmation de l'utilisateur
        }
        response = self.client.post(
            reverse('edit_game', args=[self.game1.id]), donnees_post)
        # Vérifier si la redirection est correcte maintenant
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.status_code, 302)
        self.game1.refresh_from_db()
        self.assertEqual(self.game1.name, 'Jeu Test Mis à Jour 1')
        # Vérification de l'association de la plateforme
        self.assertTrue(self.game1.platforms.filter(
            id=self.platform1.id).exists())


class StudioTests(TestCase):

    # Cette méthode s'exécutera avant chaque méthode de test
    def setUp(self):
        self.studio = Studio.objects.create(
            name="Test Studio",
            description="Ceci est un studio de test.",
            country="US"
        )

    # Test pour la page de liste des studios
    def test_studio_listing(self):
        response = self.client.get(reverse('studios'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Studio")

    # Test pour la vue de détail du studio
    def test_studio_detail(self):
        response = self.client.get(
            reverse('studio_detail', args=[self.studio.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ceci est un studio de test.")

    # Test pour le formulaire du studio
    def test_studio_form(self):
        donnees = {
            'name': 'Nouveau Studio',
            'description': 'Ceci est une nouvelle description de studio.',
            'country': 'US'
        }
        response = self.client.post(reverse('studio_form'), donnees)
        # Attendu de rediriger après la soumission réussie du formulaire
        self.assertEqual(response.status_code, 302)

    # Test pour la vue d'édition du studio
    def test_edit_studio(self):
        donnees = {
            'name': 'Studio Edité',
            'description': 'La description a été modifiée.',
            'country': 'US'
        }
        response = self.client.post(
            reverse('edit_studio', args=[self.studio.id]), donnees)
        # Attendu de rediriger après la soumission réussie du formulaire
        self.assertEqual(response.status_code, 302)


class PlatformTests(TestCase):

    # Cette méthode s'exécutera avant chaque méthode de test
    def setUp(self):
        self.platform = Platform.objects.create(
            name="Test Platform",
            description="Ceci est une plateforme de test.",
            manufacturer="Fabricant de Test"
        )

    # Test pour le formulaire de la plateforme
    def test_platform_form(self):
        donnees = {
            'name': 'Nouvelle Plateforme',
            'description': 'Ceci est une nouvelle description de plateforme.',
            'manufacturer': 'Nouveau Fabricant'
        }
        response = self.client.post(reverse('create_platform'), donnees)
        # Attendu de rediriger après la soumission réussie du formulaire
        self.assertEqual(response.status_code, 302)


class TestsDeNomsUniques(TestCase):
    def setUp(self):
        # Création d'un studio avec un nom unique pour les tests
        self.studio = Studio.objects.create(
            name="UniqueNameStudio",
            description="Ce studio a un nom unique.",
            country="US"
        )

        # Création d'un jeu avec un nom unique pour les tests
        self.game = Game.objects.create(
            name="UniqueNameGame",
            description="Ce jeu a un nom unique.",
            studio=self.studio
        )

    def test_creer_nom_studio_doublon(self):
        # Tenter de créer un autre studio avec le même nom devrait lever une IntegrityError
        with self.assertRaises(IntegrityError):
            Studio.objects.create(
                name="UniqueNameStudio",  # même nom que self.studio
                description="Ceci est un studio en double.",
                country="FR"
            )

    def test_creer_nom_jeu_doublon(self):
        # Tenter de créer un autre jeu avec le même nom devrait lever une IntegrityError
        with self.assertRaises(IntegrityError):
            Game.objects.create(
                name="UniqueNameGame",  # même nom que self.game
                description="Ceci est un jeu en double.",
                studio=self.studio
            )
