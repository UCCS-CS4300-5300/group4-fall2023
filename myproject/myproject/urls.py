"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Starwars.views import (
    HomeView,
    SelectionView,
    LoginView, 
    SignupView, 
    GameplayView, 
    ProfileView, 
    EndscreenView,
    load_characters,
    load_starships,
	Player1View,
	Player2View,
	BattleView,
	StartView
)


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
	path('selection/', SelectionView.as_view(), name='selection'),
	path('', StartView.as_view(), name='start'),
	path('player1/', Player1View.as_view(), name='player1'),
	path('player2/', Player2View.as_view(), name='player2'),
	path('battle/', BattleView.as_view(), name='battle'),
    path('gameplay/', GameplayView.as_view(), name='gameplay'),
    path('endscreen/<int:battle_id>/', EndscreenView.as_view(), name='endscreen'),
    path('admin/', admin.site.urls),
    path('load-characters/', load_characters, name='load_characters'),
    path('load-starships/', load_starships, name='load_starships'),
]

