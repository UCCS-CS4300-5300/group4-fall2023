from django.shortcuts import render
from django.views import View
from .models import Character
from django.http import JsonResponse


# Create your views here.
class HomeView(View):

  def get(self, request):
    return render(request, "home.html")


class LoginView(View):

  def get(self, request):
    return render(request, "login.html")


class SignupView(View):

  def get(self, request):
    return render(request, "signup.html")


class ProfileView(View):

  def get(self, request):
    return render(request, "profile.html")

class GameplayView(View):

  def get(self, request):
    return render(request, "gameplay.html")

def character_list(request, episode_from, episode_to):
  characters = Character.objects.filter(
      episode_from__lte=episode_from,
      episode_to__gte=episode_to
  )
  character_list = [{'name': character.name} for character in characters]
  return JsonResponse(character_list, safe=False)

