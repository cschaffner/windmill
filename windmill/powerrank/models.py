from __future__ import division
from django.db import models
from django.db.models import Q
from windmill.tools.wrapper import api_swissroundinfo
from django.conf import settings

import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.powerrank')

if settings.HOST=="http://api.playwithlv.com":
    logger.error('things here only work for leaguevine and not for playwithlv')
    raise

class TournamentManager(models.Manager):
    def add(self,tournament_id):
        # retrieve all swissrounds from tournament
        swiss=api_swissroundinfo(tournament_id,ordered=True)
        added=0
        # import all games from tournament in local db
        t,create_t=self.get_or_create(lv_id=tournament_id)
        if create_t:
            t.name=swiss['objects'][0]['tournament']['name']
            t.save()
        
        for round in swiss['objects']:
            r,create_r=Round.objects.get_or_create(lv_id=round['id'])
            if create_r:
                r.round_number=round['round_number']
            r.tournament = t
            r.save()
            for game in round['games']:
                team1,create_team1=Team.objects.get_or_create(lv_id=game['team_1_id'])
                if create_team1:
                    team1.name=game['team_1']['name']
                    team1.save()
                team2,create_team2=Team.objects.get_or_create(lv_id=game['team_2_id'])
                if create_team2:
                    team2.name=game['team_2']['name']
                    team2.save()
                gm,created_gm=Game.objects.get_or_create(lv_id=game['id'])
                gm.round=r
                gm.team_1=team1
                gm.team_2=team2
                gm.team_1_score=game['team_1_score']
                gm.team_2_score=game['team_2_score']
                gm.start_time = game['start_time']
                if game['game_site']!=None:
                    gm.field = game['game_site']['name']
                logger.info(u'added game {0} - {1} with start time {2}'.format(gm.team_1.name,gm.team_2.name,gm.start_time))
                gm.save()
            for tstand in round['standings']:
                team,create_team=Team.objects.get_or_create(lv_id=tstand['team_id'])
                st=Standing.objects.create(team=team,round=r,
                        wins=tstand['wins'], losses=tstand['losses'],
                        swiss_score=tstand['swiss_score'], swiss_rank=tstand['ranking'],
                        swiss_opponent_score=tstand['swiss_opponent_score'])
        return True
 

class Tournament(models.Model):
    objects=TournamentManager()
    
    # playwithlv.com tournament-id
    l_id = models.IntegerField(blank=True,null=True)
    # leaguevine.com tournament-id
    lv_id = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=50)

    def lgv_id(self):
        if settings.HOST=="http://api.playwithlv.com":
            return self.l_id
        elif settings.HOST=="https://api.leaguevine.com":
            return self.lv_id

    def __unicode__(self):
        return str(self.name)


class Round(models.Model):
    # playwithlv.com swissround_id
    l_id = models.IntegerField(blank=True,null=True)
    # leaguevine.com swissround_id
    lv_id = models.IntegerField(blank=True,null=True)
    
    round_number = models.IntegerField(blank=True,null=True)
    
    # many-to-one relationship between Tournament and Rounds
    tournament = models.ForeignKey(Tournament,null=True,blank=True)

    def lgv_id(self):
        if settings.HOST=="http://api.playwithlv.com":
            return self.l_id
        elif settings.HOST=="https://api.leaguevine.com":
            return self.lv_id

    def __unicode__(self):
        return u'{0} of {1}'.format(self.round_number,self.tournament)
        
class Team(models.Model):
    # playwithlv.com team-id
    l_id = models.IntegerField(blank=True,null=True)
    # leaguevine.com team-id
    lv_id = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=50)
                
    # many-to-many relationship between Teams and Rounds
    rounds = models.ManyToManyField(Round, through='Standing')


    def save(self, *args, **kwargs):
        super(Team, self).save(*args, **kwargs) # Call the "real" save() method.

    def lgv_id(self):
        if settings.HOST=="http://api.playwithlv.com":
            return self.l_id
        elif settings.HOST=="https://api.leaguevine.com":
            return self.lv_id
        
    def __unicode__(self):
        return self.name


class Game(models.Model):
    
    # playwithlv.com game-id
    l_id = models.IntegerField(null=True,blank=True)
    # leaguevine.com game-id
    lv_id = models.IntegerField(null=True,blank=True)
    
    team_1 = models.ForeignKey(Team,null=True,blank=True,related_name='game_team1')
    team_2 = models.ForeignKey(Team,null=True,blank=True,related_name='game_team2')
    
    team_1_score = models.IntegerField(null=True,blank=True)
    team_2_score = models.IntegerField(null=True,blank=True)

    # many-to-one relationship between Rounds and Game
    round = models.ForeignKey(Round,null=True,blank=True)
    
    
    start_time = models.DateTimeField(null=True,blank=True)
    field = models.CharField(max_length=50,null=True,blank=True)
    
    def lgv_id(self):
        if settings.HOST=="http://api.playwithlv.com":
            return self.l_id
        elif settings.HOST=="https://api.leaguevine.com":
            return self.lv_id

    def __unicode__(self):
        if settings.HOST=="http://api.playwithlv.com":
            return str(self.l_id)
        elif settings.HOST=="https://api.leaguevine.com":
            return str(self.lv_id)

    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs) # Call the "real" save() method.


class Standing(models.Model):
    round = models.ForeignKey(Round)
    team = models.ForeignKey(Team)
    
    wins = models.IntegerField(blank=True,null=True)
    losses = models.IntegerField(blank=True,null=True)
    swiss_score = models.IntegerField(blank=True,null=True)
    swiss_opponent_score = models.IntegerField(blank=True,null=True)
    swiss_rank = models.IntegerField(blank=True,null=True)
    power_rank = models.IntegerField(blank=True,null=True)
    strength = models.DecimalField(max_digits=6, decimal_places=4,blank=True,null=True)

    