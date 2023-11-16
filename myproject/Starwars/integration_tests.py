from unittest.mock import patch, Mock
import json
from django.test import TestCase, Client
from django.http import JsonResponse
from .views import get_character_name, load_characters, load_starships

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def read(self):
            return json.dumps(self.json_data).encode()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

    if args[0] == "https://swapi.dev/api/people/1/":  # example character URL
        return MockResponse({"name": "Luke Skywalker"}, 200)
    elif args[0] == "https://swapi.dev/api/films/1/":  # example film URL
        return MockResponse({"characters": ["https://swapi.dev/api/people/1/"]}, 200)
    elif args[0] == "https://swapi.dev/api/people/2/starships/":  # example starship URL
        return MockResponse([{"name": "X-wing", "model": "T-65 X-wing"}], 200)

    return MockResponse(None, 404)

class GetCharacterNameTest(TestCase):
  @patch('urllib.request.urlopen', side_effect=mocked_requests_get)
  def test_get_character_name(self, mock_get):
      character_name = get_character_name("https://swapi.dev/api/people/1/")
      self.assertEqual(character_name, "Luke Skywalker")

class LoadCharactersTest(TestCase):
  @patch('urllib.request.urlopen', side_effect=mocked_requests_get)
  def test_load_characters(self, mock_get):
      response = load_characters(Mock(GET={'episode_id': '1'}))
      self.assertEqual(response.status_code, 200)
      self.assertEqual(json.loads(response.content), [{"name": "Luke Skywalker", "url": "https://swapi.dev/api/people/1/"}])

class LoadStarshipsTest(TestCase):
    @patch('Starwars.views.urllib.request.urlopen')
    def test_load_starships(self, mock_urlopen):
        # Mock the response for the character API call
        mock_character_response = Mock()
        mock_character_response.read.return_value = json.dumps({
            'starships': [
                "https://swapi.dev/api/starships/12/"
            ]
        }).encode('utf-8')

        # Mock the response for the starship API call
        mock_starship_response = Mock()
        mock_starship_response.read.return_value = json.dumps({
            "name": "Death Star",
            "model": "DS-1 Orbital Battle Station"
        }).encode('utf-8')

        # Set up the side effect for the mock_urlopen to handle multiple calls
        mock_urlopen.side_effect = [mock_character_response, mock_starship_response]

        # Make a request to your view
        client = Client()
        response = client.get('/load-starships/', {'character_id': '1'})

        # Check the response
        self.assertEqual(response.status_code, 500, msg=f"Expected status code 500, but got {response.status_code}")