from __future__ import division
from django.db import models
from windmill.tools.wrapper import *
import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


class Tournament(models.Model):
    l_id = models.IntegerField()
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.name)

class GameManager(models.Manager):
    def addmatches(self,tournament_id):
        # retrieve all games from tournament
        games=api_gamesbytournament(tournament_id)
        logger.info(games)
        added=0
        # import all games from tournament in local db
        for g in games['objects']:
            # create or get tournament
            t,create_t=Tournament.objects.get_or_create(l_id=g['tournament']['id'])
            if create_t:
                t.name = g['tournament']['name']
                t.save()

            gm,created=self.get_or_create(l_id=g['id'])
            if created:
                added+=1
            if g['team_1_id'] is not None:            
                gm.team_1_id=g['team_1_id']
                gm.team_1_name=g['team_1']['name']
            if g['team_2_id'] is not None:            
                gm.team_2_id=g['team_2_id']
                gm.team_2_name=g['team_2']['name']
            # link game with tournament
            gm.tournament=t            
            gm.start_time = g['start_time']
            # gm.field = g['field']
            logger.info('added game {0} - {1}'.format(g['team_1_id'],g['team_2_id']))
            gm.save()
        return added

class Game(models.Model):
    objects=GameManager()
    
    # leaguevine game-id
    l_id = models.IntegerField()
    
    team_1_id = models.IntegerField(null=True,blank=True)
    team_2_id = models.IntegerField(null=True,blank=True)
    
    team_1_name = models.CharField(max_length=50,null=True,blank=True)
    team_2_name = models.CharField(max_length=50,null=True,blank=True)

    # many-to-one relationship between Tournaments and Teams
    tournament = models.ForeignKey(Tournament,null=True,blank=True)
    
    start_time = models.DateTimeField(null=True,blank=True)
    field = models.CharField(max_length=50,null=True,blank=True)
    
    # totals
    team_1_spirit = models.IntegerField(null=True,verbose_name="Team1's received spirit",blank=True)
    team_2_spirit = models.IntegerField(null=True,verbose_name="Team2's received spirit",blank=True)

    # todo: when teams are filling in the sheets, we will more detailed categories:
    # team1_rules
    # team1_fouls
    # team1_fairmind
    # team1_positive
    # team1_compare

    def __unicode__(self):
        return str(self.l_id)

    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs) # Call the "real" save() method.
        if self.team_1_spirit is not None:
            # update team1
            t,create=Team.objects.get_or_create(l_id=self.team_1_id)
            if create:
                t.name=self.team_1_name
                t.tournament=self.tournament
            t.add_received(self.team_1_spirit)
            if self.team_2_spirit is not None:
                t.add_given(self.team_2_spirit)
            t.update_spirit()            
            t.save()
        
        if self.team_2_spirit is not None:
            # update team2
            t,create=Team.objects.get_or_create(l_id=self.team_2_id)
            if create:
                t.name=self.team_2_name
                t.tournament=self.tournament
            t.add_received(self.team_2_spirit)
            if self.team_1_spirit is not None:
                t.add_given(self.team_1_spirit)
            t.update_spirit()            
            t.save()        
         

class Team(models.Model):
    # leaguevine team-id
    l_id = models.IntegerField()
    name = models.CharField(max_length=50)
    
    # many-to-one relationship between Tournaments and Teams
    tournament = models.ForeignKey(Tournament,null=True,blank=True)
    
    # spirit scores
    received = models.CommaSeparatedIntegerField(max_length=30)
    given = models.CommaSeparatedIntegerField(max_length=30)
    
    avg_received = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    avg_given = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    nr_received = models.IntegerField(null=True,blank=True)
    nr_given = models.IntegerField(null=True,blank=True)
        
    def add_received(self,score):
        if self.received=='':
            self.received=str(score)
        else:
            self.received += ','
            self.received += str(score)

    def add_given(self,score):
        if self.given=='':
            self.given=str(score)
        else:
            self.given += ','
            self.given += str(score)
    
    def update_spirit(self):
        self.nr_received,self.avg_received=self.compute(self.received)
        self.nr_given,self.avg_given=self.compute(self.given)
    
    def compute(self,cslist):
        import re
        if cslist=='':
            return 0,None
        count=0
        total=0
        for el in re.split(r',',cslist):
            try:
                i=int(el)
                count+=1
                total+=i
            except:
                logger.error('only integers should be stored in list of spirit scores')
                raise            
        if count>0:
            return count,total/count
        else:
            return 0,None

        
    def __unicode__(self):
        return str(self.name)

