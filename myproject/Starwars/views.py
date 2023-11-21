from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Character
from django.http import JsonResponse
from .forms import StarWarsForm
import urllib.request
import json
from django.core.exceptions import ObjectDoesNotExist
import os


def load_json_data(file_name):
  base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  json_file_path = os.path.join(base_dir, file_name)
  with open(json_file_path, 'r', encoding='utf-8') as file:
      return json.load(file)

# Load the JSON data at the start of the application
starwars_data = load_json_data('starwars_data.json')


# Create your views here.
class HomeView(View):

  def get(self, request):
    return render(request, "home.html")


class LoginView(View):

  def get(self, request):
    return render(request, "login.html")


class StartView(View):

  def get(self, request):
    return render(request, "start.html")


class Player1View(View):

  def get(self, request):
    return render(request, "player1.html")


class Player2View(View):

  def get(self, request):
    return render(request, "player2.html")


class BattleView(View):

  def get(self, request):
    return render(request, "battle.html")


class SelectPlayer2View(View):

  def get(self, request):
    return render(request, "selectPlayer2.html")


class SignupView(View):

  def get(self, request):
    return render(request, "signup.html")


class SelectionView(View):

  def get(self, request):
    return render(request, "selection.html")


class ProfileView(View):

  def get(self, request):
    return render(request, "profile.html")


class GameplayView(TemplateView):
  template_name = "gameplay.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = StarWarsForm()  # Add the form to the context
    return context


class EndscreenView(View):

  def get(self, request, battle_id):
    battle = Battle.objects.get(id=battle_id)
    characters = Character.objects.filter(episode_from__lte=battle.episode_to,
                                          episode_to__gte=battle.episode_from)
    context = {
        'win_status': 'You Win' if battle.won else 'You Lose',
        'battle_details': battle.details,
        'characters': characters
    }
    return render(request, 'endscreen.html', context)


def get_character_name(character_url):
  with urllib.request.urlopen(character_url) as response:
    character_data = json.loads(response.read().decode())
    return character_data['name']


def load_characters(request):
  episode_id = request.GET.get('episode_id')

  if not episode_id:  # Check if episode_id is not empty
    return JsonResponse(
        [], safe=False)  # Return an empty list or handle as appropriate

  try:
    characters = Character.objects.filter(episodes__id=episode_id)
    characters_data = [{
        'name': character.name,
        'id': character.id
    } for character in characters]
    return JsonResponse(characters_data, safe=False)
  except Exception as e:
    print(f'An error occurred: {e}')
    return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)


def load_starships(request):
  character_id = request.GET.get('character_id')

  try:
    character = Character.objects.get(id=character_id)
    starships = character.starships.all()
    starships_data = [{
        'name': starship.name,
        'id': starship.id
    } for starship in starships]
    return JsonResponse(starships_data, safe=False)
  except Character.DoesNotExist:
    return JsonResponse({'error': 'Character not found.'}, status=404)
  except Exception as e:
    print(f'An error occurred: {e}')
    return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)


def get_characters_from_episode(episode_id):
  try:
    episode = Episode.objects.get(id=episode_id)
    characters = episode.characters.all()
    return [character.name for character in characters]
  except Episode.DoesNotExist:
    return []


def get_starships_for_character(character_id):
  try:
    character = Character.objects.get(id=character_id)
    starships = character.starships.all()
    return [starship.name for starship in starships]
  except Character.DoesNotExist:
    return []


def your_view(request):
  form = StarWarsForm()
  return render(request, 'your_template.html', {'form': form})
