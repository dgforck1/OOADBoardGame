from django.db import models

# Create your models here.

class pending_games(models.Model):
    name = models.CharField(max_length=1)
    def __unicode__(self):
        return self.name

class game_results(models.Model):
    game = models.IntegerField()
    history = models.CharField(max_length=9)
    def __unicode__(self):
        return self.history
    
