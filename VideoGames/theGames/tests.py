from django.test import TestCase
from django.urls import reverse
from .models import Game, Studio

class GameTests(TestCase):

    def setUp(self):
        # Create Studios
        self.test_studio = Studio.objects.create(
            name="Test Studio",
            description="This is a test studio",
            country="US"
        )
        
        self.another_test_studio = Studio.objects.create(
            name="Another Test Studio",
            description="This is another test studio",
            country="US"
        )

        # Create Games with the Studios
        self.game1 = Game.objects.create(
            name="Test Game 1",
            description="This is a test game",
            studio=self.test_studio
        )
        self.game2 = Game.objects.create(
            name="Test Game 2",
            description="This is another test game",
            studio=self.another_test_studio
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
            'studio': self.game1.id,
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
            'studio': self.game1.id,
        })
        self.assertEqual(response.status_code, 302)
        self.game1.refresh_from_db()
        self.assertEqual(self.game1.name, 'Updated Test Game 1')

class StudioTests(TestCase):

# This method will run before each test method
    def setUp(self):
        self.studio = Studio.objects.create(
            name="Test Studio",
            description="This is a test studio.",
            country="US"
        )

    # Test for the studio listing page
    def test_studio_listing(self):
        response = self.client.get(reverse('studios'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Studio")
        
    # Test for the studio detail view
    def test_studio_detail(self):
        response = self.client.get(reverse('studio', args=[self.studio.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a test studio.")
        
    # Test for the studio form
    def test_studio_form(self):
        data = {
            'name': 'New Studio',
            'description': 'This is a new studio description.',
            'country': 'US'
        }
        response = self.client.post(reverse('studio_form'), data)
        self.assertEqual(response.status_code, 302)  # Expected to redirect after successful form submission
        
    # Test for studio edit view
    def test_edit_studio(self):
        data = {
            'name': 'Edited Studio',
            'description': 'Description has been edited.',
            'country': 'US'
        }
        response = self.client.post(reverse('edit_studio', args=[self.studio.id]), data)
        self.assertEqual(response.status_code, 302)  # Expected to redirect after successful form submission
        
    # Test for studio delete view
    def test_delete_studio(self):
        response = self.client.post(reverse('studio_delete', args=[self.studio.id]))
        self.assertEqual(response.status_code, 302)  # Expected to redirect after successful deletion
        with self.assertRaises(Studio.DoesNotExist):
            Studio.objects.get(pk=self.studio.id)
