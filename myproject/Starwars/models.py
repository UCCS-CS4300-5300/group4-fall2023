from django.db import models

# Create your models here.
class Character(models.Model):
  name = models.CharField(max_length=100)
  episode_from = models.IntegerField()
  episode_to = models.IntegerField()

  def __str__(self):
      return self.name