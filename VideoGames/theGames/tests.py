from django.test import TestCase
from django.urls import reverse
from .models import Game

class GameTests(TestCase):

    def setUp(self):
        self.game1 = Game.objects.create(
            name="Test Game 1",
            description="This is a test game",
            studio="Test Studio"
        )
        self.game2 = Game.objects.create(
            name="Test Game 2",
            description="This is another test game",
            studio="Another Test Studio"
        )

    def test_game_listing_view(self):
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game 1')
        self.assertContains(response, 'Test Game 2')

    def test_game_detail_view_valid_game(self):
        response = self.client.get(reverse('game', args=[self.game1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game 1')

    def test_game_detail_view_invalid_game(self):
        response = self.client.get(reverse('game', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_game_form_view_get(self):
        response = self.client.get(reverse('game_form'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form') # Checking for a form tag

    def test_game_form_view_post(self):
        response = self.client.post(reverse('game_form'), {
            'name': 'Test Game 3',
            'description': 'A third test game.',
            'studio': 'Third Test Studio',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Game.objects.filter(name='Test Game 3').exists())

    def test_game_delete_view_get(self):
        response = self.client.get(reverse('game_delete', args=[self.game1.id]))
        self.assertEqual(response.status_code, 200)

    def test_game_delete_view_post(self):
        response = self.client.post(reverse('game_delete', args=[self.game1.id]))
        self.assertEqual(response.status_code, 302)  # Assuming a redirect after deletion
        self.assertFalse(Game.objects.filter(id=self.game1.id).exists())

    def test_game_edit_view_get(self):
        response = self.client.get(reverse('edit_game', args=[self.game1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game 1')

    def test_game_edit_view_post(self):
        response = self.client.post(reverse('edit_game', args=[self.game1.id]), {
            'name': 'Updated Test Game 1',
            'description': 'Updated description.',
            'studio': 'Updated Test Studio',
        })
        self.assertEqual(response.status_code, 302)
        self.game1.refresh_from_db()
        self.assertEqual(self.game1.name, 'Updated Test Game 1')
