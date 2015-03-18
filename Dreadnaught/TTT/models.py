from django.db import models



class users(models.Model):
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=50, default='')
    ip_address = models.CharField(max_length=15)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    def __unicode__(self):
        return self.user_name


class scripts(models.Model):
    user_id = models.ForeignKey(users)
    name = models.CharField(max_length=50, default='')
    location = models.CharField(max_length=255, default='')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)    
    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('user_id', 'name')


class game(models.Model):
    player1 = models.ForeignKey(users, blank=True, null=True, \
                                related_name='p1')
    player2 = models.ForeignKey(users, blank=True, null=True, \
                                related_name='p2')
    ai1script = models.ForeignKey(scripts, blank=True, null=True, \
                                  related_name='s1')
    ai2script = models.ForeignKey(scripts, blank=True, null=True, \
                                  related_name='s2')
    state = models.IntegerField(default=0)
        #0: pending, 1: x's turn, 2: o's turn, 3: x won, 4: o won, 5: draw
    history = models.CharField(max_length=9, default='')
    def __unicode__(self):
        return self.state




#the models below this line are depricated
class pending_games(models.Model):
    name = models.CharField(max_length=1)
    def __unicode__(self):
        return self.name

class game_results(models.Model):
    game = models.IntegerField()
    history = models.CharField(max_length=9)
    def __unicode__(self):
        return self.history
    
