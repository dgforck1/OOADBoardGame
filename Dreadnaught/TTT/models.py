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
    time_left = models.FloatField(default=900000.0)

    def __unicode__(self):
        return str(self.id)


class turns(models.Model):
    game = models.ForeignKey(game, related_name='g', blank=False, null=False)
    turn_num = models.IntegerField(default=0)
    begin_state = models.CharField(max_length=100, default='', null=False)
    accumulated_time = models.FloatField(default=0.0)


class moves(models.Model):
    turn_num = models.ForeignKey(turns, related_name='turn', blank=False, null=False)
    move_num = models.IntegerField(default=0)
    sx = models.IntegerField(default=0)
    sy = models.IntegerField(default=0)
    dx = models.IntegerField(default=0)
    dy = models.IntegerField(default=0)



    
