from __future__ import division
from django.db import models
from django.db.models import Q
from windmill.tools.wrapper import api_swissroundinfo
from power import strength
from django.conf import settings
from operator import itemgetter
import os

import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.powerrank')

if settings.HOST=="http://api.playwithlv.com":
    logger.error('things here only work for leaguevine and not for playwithlv')
    raise

class TournamentManager(models.Manager):
    def add(self,tournament_id):
        from datetime import datetime
        # create a new directory for the output of this routine
        output_path='{0}/static/output/{1:%Y%m%d_%H%M%S%f}'.format(settings.ROOT_PATH,datetime.now())
        os.mkdir(output_path)

        # retrieve all swissrounds from tournament
        swiss=api_swissroundinfo(tournament_id,ordered=True)
        added=0
        # import all games from tournament in local db
        t,create_t=self.get_or_create(lv_id=tournament_id)
        if create_t:
            t.name=swiss['objects'][0]['tournament']['name']
            t.save()
        
        games=[]
        for round in swiss['objects']:
            r,create_r=Round.objects.get_or_create(lv_id=round['id'])
            if create_r:
                r.round_number=round['round_number']
            r.tournament = t
            r.save()

            # account with offset for less teams in later rounds                    
            if round['round_number']==1:
                nrteams=len(round['standings'])
            offset=nrteams-len(round['standings'])            
 
            # extend standings with chris-rank (sorted first according to swiss_score, wins, fewest losses, swiss_opponent_scores etc.)
            # and mark-ranks (sorted first according to wins, then swiss_score, swiss_opponent_scores)
            # notice the reversed order of sorting, first the least important key, then more and more important ones
            mark_sort=sorted(round['standings'],key=lambda x:int(x['swiss_opponent_score']),reverse=True)
            mark_sort=sorted(mark_sort,key=lambda x:int(x['swiss_score']),reverse=True)
            mark_sort=sorted(mark_sort,key=lambda x:int(x['wins']),reverse=True)
            for rank,tstand in enumerate(mark_sort,1):
                tstand['mark_rank']=rank+offset

            chris_sort=sorted(mark_sort,key=lambda x:int(x['swiss_opponent_score']),reverse=True)
            chris_sort=sorted(chris_sort,key=lambda x:int(x['losses']))
            chris_sort=sorted(chris_sort,key=lambda x:int(x['wins']),reverse=True)
            chris_sort=sorted(chris_sort,key=lambda x:int(x['swiss_score']),reverse=True)
            for rank,tstand in enumerate(chris_sort,1):
                tstand['chris_rank']=rank+offset
                        
            for tstand in chris_sort:
                team=Team.objects.get(lv_id=tstand['team_id'])
                st,create_st=Standing.objects.get_or_create(team=team,round=r)
                st.wins=tstand['wins']
                st.losses=tstand['losses']
                st.swiss_score=tstand['swiss_score']
                st.swiss_opponent_score=tstand['swiss_opponent_score']
                st.mark_rank=tstand['mark_rank']
                st.chris_rank=tstand['chris_rank']
                if abs(tstand['chris_rank']-(tstand['ranking']+offset))>1:
                    logger.error(u'team: {0}, chris_rank: {1}, ranking: {2}'.format(tstand['team']['name'],tstand['chris_rank'],tstand['ranking']+offset))
                st.save()
                      
            games.extend(round['games'])
            strength_stand=strength(games,output_path)
            for sstand in strength_stand:
                team=Team.objects.get(lv_id=sstand['team_id'])
                st,create_st=Standing.objects.get_or_create(team=team,round=r)
                st.strength=sstand['strength']
                st.power_rank=sstand['ranking']
                st.save()

            for game in round['games']:
                if game['team_1_score']>0 or game['team_2_score']>0:
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
                    team_1_strength=team1.standing_set.get(round=r).strength
                    team_2_strength=team2.standing_set.get(round=r).strength                    
                    gm.pred_margin_current=(team_1_strength -  team_2_strength)
                    logger.info(u'added game {0} - {1} with pred_margin {2}'.format(gm.team_1.name,gm.team_2.name,gm.pred_margin_current))
                    gm.save()


        # update the overall upsets of all games
        # assuming r is the round-object of the last round
        for gm in Game.objects.filter(round__tournament=t):
            team_1_strength=gm.team_1.standing_set.get(round=r).strength
            team_2_strength=gm.team_2.standing_set.get(round=r).strength                    
            gm.pred_margin_overall=(team_1_strength -  team_2_strength)
            gm.save()
        return True
 
    def top8_ranks(self):
        # make a figure with the rank curves of the top8 teams
        pass
        

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
        return u'{0}'.format(self.round_number)
        
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
    
    # score margin predicted base on all games up to this round
    pred_margin_current=models.DecimalField(max_digits=6, decimal_places=4,blank=True,null=True)
    upset_current=models.DecimalField(max_digits=7, decimal_places=4,blank=True,null=True)
    # same thing but computed based on all games of this tournament
    pred_margin_overall=models.DecimalField(max_digits=6, decimal_places=4,blank=True,null=True)
    upset_overall=models.DecimalField(max_digits=7, decimal_places=4,blank=True,null=True)
    
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
        self.upset_current = ((self.team_1_score - self.team_2_score) - self.pred_margin_current)**2
        self.upset_overall = ((self.team_1_score - self.team_2_score) - self.pred_margin_overall)**2
        super(Game, self).save(*args, **kwargs) # Call the "real" save() method.


class Standing(models.Model):
    round = models.ForeignKey(Round)
    team = models.ForeignKey(Team)
    
    wins = models.IntegerField(blank=True,null=True)
    losses = models.IntegerField(blank=True,null=True)
    swiss_score = models.IntegerField(blank=True,null=True)
    swiss_opponent_score = models.IntegerField(blank=True,null=True,verbose_name='opp_score')
    chris_rank = models.IntegerField(blank=True,null=True)
    mark_rank = models.IntegerField(blank=True,null=True)
    power_rank = models.IntegerField(blank=True,null=True)
    strength = models.DecimalField(max_digits=6, decimal_places=4,blank=True,null=True)

    