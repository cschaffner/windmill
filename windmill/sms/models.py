from django.db import models
from windmill.tools.models import Team
import logging
import datetime
from windmill.tools.wrapper import *


# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


class Tournament(models.Model):
    # playwithlv.com tournament id
    l_id = models.IntegerField(blank=True,null=True)
    # leaguevine.com tournament id
    lv_id = models.IntegerField(blank=True,null=True)
    
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.name)

class SMSManager(models.Manager):
    def broadcast(self,message):
        # send SMS with message
        # to all registered phone numbers
        
        # get a list of all phone numbers
        for t in Team.objects.all():
            for nr in t.mobilenr():
                logger.info(nr)
    
    
    def clear_round(self,round_nr,tournament_id):
        """ 
        delete all SMS with a particular round_nr and tournament_id
        """
#        self.delete(round_nr=)
        return True
        
    def swiss_round(self,swiss,round_nr,tournament):
        """
        GOAL: 
        
        Swissdraw:
        $text = "Welcome to Windmill Windup 2012!In round 1,";
        
        After a 15-2 loss in round 1, you are now ranked 12th. In round 2,
        you'll play "Ultimate Kaese" (ranked 13th) on Field 1 at 12:30.
        """   
    
        prevRound={}
        for r in swiss['objects']:
            if round_nr > 1 and r['round_number']==(round_nr-1):
                prevRound=r
            elif r['round_number']==round_nr:
                thisRound=r
        # make sure this tournament actually exists in the database
        if settings.HOST=="playwithlv.com":
            tourney,created=Tournament.objects.get_or_create(l_id = tournament['id'])
        elif settings.HOST=="leaguevine.com":
            tourney,created=Tournament.objects.get_or_create(lv_id = tournament['id'])
        if created:
            tourney.name = tournament['name']
            tourney.save()
        
        nr_created=0
        vp_bye = tournament['swiss_points_for_bye']
        # go through all games in this round and create SMS for team_1 and team_2
        for g in thisRound['games']:
            if g['team_1'] is not None:
                msg=self.msg_swiss_team(prevRound,thisRound,g['team_1'],g['team_2'],g['start_time'],vp_bye) # TODO: Field
                if settings.HOST=="playwithlv.com":
                    team_obj=Team.objects.get(l_id = g['team_1_id'])
                elif settings.HOST=="leaguevine.com":
                    team_obj=Team.objects.get(lv_id = g['team_1_id'])
                sms = SMS.objects.create(message = msg,
                                         team = team_obj,
                                         round_id = thisRound['round_number'],
                                         tournament = tourney,
                                         status = 1,
                                         createTime = '2012-05-02T15:33:21+00:00')
                nr_created += 1
            if g['team_2'] is not None:
                msg=self.msg_swiss_team(prevRound,thisRound,g['team_2'],g['team_1'],g['start_time'],vp_bye) # TODO: Field
                if settings.HOST=="playwithlv.com":
                    team_obj=Team.objects.get(l_id = g['team_2_id'])
                elif settings.HOST=="leaguevine.com":
                    team_obj=Team.objects.get(lv_id = g['team_2_id'])
                sms = SMS.objects.create(message = msg,
                                         team = team_obj,
                                         round_id = thisRound['round_number'],
                                         tournament = tourney,
                                         status = 1,
                                         createTime = '2012-05-02T15:33:21+00:00')
                nr_created += 1
        
        return nr_created
            
        
    def msg_swiss_team(self,prevRound,thisRound,team,opp,start_time,vp_bye):
        if not prevRound.__contains__('round_number'):
            msg=u'Welcome to Windmill Windup 2012! In Round 1,'
            tomorrow=False
        else:
            tomorrow=True # TODO: figure out if this round's game is day later compared to prevRound
            msg=u'After a {0} '.format(result_in_swissround(prevRound,team['id']))
            msg += u'in round {0}, '.format(prevRound['round_number'])

        if thisRound['round_number']<9: 
            msg += u'you are now ranked {0}.'.format(rank_in_swissround(prevRound,team['id']))
            msg += u'In round {0}'.format(thisRound['round_number']) + ','
            if opp is None:
                msg += u"you can take a break due to the odd number of teams.You'll score {0} victory points.".format(vp_bye)
            else:
                msg += u"you'll play {0} ".format(opp['name'])
                msg += u"(ranked {0}) ".format(rank_in_swissround(prevRound,opp['id']))            
                msg += u"on Field ?? "
                if tomorrow:
                    msg += u'tomorrow '
                msg += u"at {0}".format(start_time)
            if tomorrow:
                msg += u"Pls hand in today's spirit scores."
        else: # last round
            msg += u'you finish Windmill 2012 in rank {0}, congrats!'.format(rank_in_swissround(prevRound,team['id']))
            msg += u'Please hand in all spirit scores and see you next year!'
        
        return msg
    
    
        
        
class SMS(models.Model):
    objects = SMSManager()
    
    team = models.ForeignKey(Team,null=True,blank=True)
    round_id = models.IntegerField()
    # many-to-one relationship between Tournaments and SMS
    tournament = models.ForeignKey(Tournament,null=True,blank=True)
    message = models.CharField(max_length=540,null=True,blank=True) # 3*180 = 540
    status = models.IntegerField(null=True,blank=True)
    createTime = models.DateTimeField(null=True,blank=True)
    submitTime = models.DateTimeField(null=True,blank=True)
    sentTime = models.DateTimeField(null=True,blank=True)
    receivedTime = models.DateTimeField(null=True,blank=True)
    

    def __unicode__(self):
        return str(self.id)

