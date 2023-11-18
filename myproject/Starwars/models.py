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
    won = models.BooleanField(default=False)
    details = models.TextField()
    episode_from = models.IntegerField()
    episode_to = models.IntegerField()
  
    def __str__(self):
        return "Battle Won: " + str(self.won) + ", Details: " + self.details

# Define the CharactersStarship model
class CharactersStarship(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    starship = models.ForeignKey(Starship, on_delete=models.CASCADE)
