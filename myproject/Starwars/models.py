from django.db import models


class Episode(models.Model):
  episode_number = models.IntegerField(unique=True)
  title = models.CharField(max_length=100)

  def __str__(self):
    return f"Episode {self.episode_number}: {self.title}"


class Starship(models.Model):
  name = models.CharField(max_length=100)
  attack = models.IntegerField(default=0)
  defend = models.IntegerField(default=0)
  dodge = models.IntegerField(default=0)

  def __str__(self):
    return self.name


class Character(models.Model):
  name = models.CharField(max_length=100)
  starships = models.ManyToManyField('Starship', blank=True)
  episodes = models.ManyToManyField('Episode', blank=True)

  def __str__(self):
    return self.name


# Define the Battle model
class Battle(models.Model):
  won = models.CharField(max_length=1)
  player1_character = models.ForeignKey(Character,
                                        related_name='player1_character',
                                        on_delete=models.CASCADE,
                                        null=True)
  player1_starship = models.ForeignKey(Starship,
                                       related_name='player1_starship',
                                       on_delete=models.CASCADE,
                                       null=True)
  player2_character = models.ForeignKey(Character,
                                        related_name='player2_character',
                                        on_delete=models.CASCADE,
                                        null=True)
  player2_starship = models.ForeignKey(Starship,
                                       related_name='player2_starship',
                                       on_delete=models.CASCADE,
                                       null=True)

  def __str__(self):
    win_status = "Player 1 Wins" if self.won == '1' else self.won == '2' "Player 2 Wins"
    return f"Battle {win_status}: {self.player1_character} in {self.player1_starship} vs {self.player2_character} in {self.player2_starship}"


# Define the CharactersStarship model
class CharactersStarship(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  starship = models.ForeignKey(Starship, on_delete=models.CASCADE)
