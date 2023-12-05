from django.test import TestCase
from .models import Character  
from django.urls import reverse

class CharacterModelTest(TestCase):

    def test_character_str_representation(self):
        # Create a Character object
        character = Character(name="Test Character", episode_from=1, episode_to=10)

        # Check if the string representation of the Character is correct
        self.assertEqual(str(character), "Test Character")

class ViewsTest(TestCase):

    def test_home_view(self):
        rgit push origin --tags esponse = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_gameplay_view(self):
        response = self.client.get(reverse('gameplay'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gameplay.html')

