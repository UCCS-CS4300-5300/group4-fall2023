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
from django.shortcuts import render, redirect
from .models import Episode, Character, Starship, Player
from django.http import HttpResponse

TIMELINE_TO_FILM_IDS = {
    '4': [1, 2, 3],  # Episode 1-3
    '1': [4, 5, 6],  # Episode 4-6
}


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
  url = f'https://swapi.dev/api/films/{episode_id}/'

  try:
    with urllib.request.urlopen(url) as response:
      data = json.loads(response.read().decode())
      characters_urls = data.get('characters', [])
      characters = []
      for character_url in characters_urls:
        character_name = get_character_name(character_url)
        characters.append({'name': character_name, 'url': character_url})
      return JsonResponse(characters, safe=False)
  except urllib.error.HTTPError as e:
    # Log error
    print(f'HTTPError: {e.code} for film ID: {episode_id}')
    return JsonResponse({'error': 'The requested resource was not found.'},
                        status=404)
  except Exception as e:
    # Log any other exceptions
    print(f'An error occurred: {e}')
    return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)


def load_starships(request):
  character_id = request.GET.get('character_id')
  url = f'https://swapi.dev/api/people/{character_id}/'

  try:
    with urllib.request.urlopen(url) as response:
      character_data = json.loads(response.read().decode())
      starship_urls = character_data.get('starships', [])
      starships = []
      for starship_url in starship_urls:
        with urllib.request.urlopen(starship_url) as response:
          starship_data = json.loads(response.read().decode())
          starships.append({
              'name': starship_data['name'],
              'model': starship_data['model']
          })
      return JsonResponse(starships, safe=False)
  except urllib.error.HTTPError as e:
    print(
        f'HTTPError: {e.code} when fetching starships for character ID: {character_id}'
    )
    return JsonResponse({'error': 'Starship resource not found.'},
                        status=e.code)
  except Exception as e:
    print(f'An error occurred: {e}')
    return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)


def get_characters_from_episode(episode_id):
  url = f'https://swapi.dev/api/films/{episode_id}/'
  with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())
    characters = data.get('characters', [])
    return characters


def get_starships_for_character(character_id):
  url = f'https://swapi.dev/api/people/{character_id}/'
  with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())
    starships = data.get('starships', [])
    return starships


def player1_data(request):
  if request.method == 'POST':
    # Get data from the form
    episode_id = request.POST.get('timeline1')
    character_id = request.POST.get('character1')
    starship_id = request.POST.get('starship1')

    # Fetch the corresponding objects from the database
    episode = Episode.objects.get(id=episode_id)
    character = Character.objects.get(id=character_id)
    starship = Starship.objects.get(id=starship_id)

    # Create and save the Player instance
    player = Player(chosen_episode=episode,
                    chosen_character=character,
                    chosen_starship=starship)
    player.save()

    # Redirect to player 2 form or another view
    return HttpResponse("Player 2 data processed")

  return render(request, 'player1.html')


def player2_data(request):
  if request.method == 'POST':
    # Get data from the form
    episode_id = request.POST.get('timeline2')
    character_id = request.POST.get('character2')
    starship_id = request.POST.get('starship2')

    # Fetch the corresponding objects from the database
    episode = Episode.objects.get(id=episode_id)
    character = Character.objects.get(id=character_id)
    starship = Starship.objects.get(id=starship_id)

    # Create and save the Player instance
    player = Player(chosen_episode=episode,
                    chosen_character=character,
                    chosen_starship=starship)
    player.save()
    return HttpResponse("Player 2 data processed")

  return render(request, 'player2.html')


def some_other_view(request):
  player1_data = request.session.get('player1_data', {})
  player2_data = request.session.get('player2_data', {})
  context = {'player1_data': player1_data, 'player2_data': player2_data}
  return render(request, 'another_template.html', context)


def your_view(request):
  form = StarWarsForm()
  return render(request, 'your_template.html', {'form': form})
