from django.db import models
from windmill.tools.models import Team, Tournament
import logging
from datetime import datetime
from windmill.tools.wrapper import *
# Import the SmsCity Library which will send the message to our server
from SmsCity import SmsCity
from random import getrandbits


# Get an instance of a logger
logger = logging.getLogger('windmill.sms')

def ordinal(n):
    n=int(n)  # only works if string can be properly converted to an integer
    if 10 < n < 14: return u'%sth' % n
    if n % 10 == 1: return u'%sst' % n
    if n % 10 == 2: return u'%snd' % n
    if n % 10 == 3: return u'%srd' % n
    return u'%sth' % n


class SMSManager(models.Manager):
    def sendSmsCity(self):
        # sends all SMS with status 1 to SmsCity
        
        # setup a test-SMS:
        sms = SMS.objects.create(message='this is just a test',number='31619091702',status=u'ready')
                
        
        # Set the SMScity username and password, and create an instance of the SmsCity class
        smsApi = SmsCity('windmill', '2smscity')
        
        # Set the sender, could be an number (16 numbers) or letters (11 characters)
        smsApi.setSender('WW_2012')
        
        # Add the destination mobile number.
        # This method can be called several times to add have more then one recipient for the same message
        smsApi.addDestination(sms.number)
        
        # Set an reference
#        ref=getrandbits(63)
        smsApi.setReference(sms.id)
        
        # Send the message to the destination(s)
        smsApi.sendSms(sms.message)
        
        # When using in the console, it will show you what the response was from our server
        logger.info('Response: {0}'.format(smsApi.getResponseCode()))
        logger.info('{0}'.format(smsApi.getResponseMessage()))
        logger.info('{0}'.format(smsApi.getCreditBalance()))

        sms.responseCode=smsApi.getResponseCode()
        sms.responseMessage=smsApi.getResponseMessage()
        sms.save()
        
        return smsApi.getResponseCode()

    
    def broadcast(self,message):
        # send SMS with message
        # to all registered phone numbers
        
        nr_created=0
        for t in Team.objects.all():
            for nr in t.mobilenr():
                sms = SMS.objects.create(team=t,tournament=t.tournament,
                                         message=message,number=nr,status=u'ready')
                logger.info('new sms with id {0} created'.format(sms.id))
                nr_created += 1
        return nr_created
    
    def sendSMS(self,message,target):
        # send SMS with message
        # to all teams with id in target array

        nr_created=0
        for t_id in target:
            t=Team.objects.get(id=t_id)
            for nr in t.mobilenr():
                sms = SMS.objects.create(team=t,tournament=t.tournament,
                                         message=message,number=nr,status=u'ready')
                logger.info('new sms with id {0} created'.format(sms.id))
                nr_created += 1
        
        return nr_created
    
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
        # retrieve the tournament from the database
        # assumes that those tournaments already exist there
        if settings.HOST=="http://api.playwithlv.com":
            tourney=Tournament.objects.get(l_id = tournament['id'])
        elif settings.HOST=="https://api.leaguevine.com":
            tourney=Tournament.objects.get(lv_id = tournament['id'])
        
        nr_created=0
        vp_bye = tournament['swiss_points_for_bye']
        # go through all games in this round and create SMS for team_1 and team_2
        for g in thisRound['games']:
            if g['team_1'] is not None:
                msg=self.msg_swiss_team(prevRound,thisRound,g['team_1'],g['team_2'],g['start_time'],g['game_site']['name'],vp_bye) 
                if settings.HOST=="http://api.playwithlv.com":
                    team_obj=Team.objects.get(l_id = g['team_1_id'])
                elif settings.HOST=="https://api.leaguevine.com":
                    team_obj=Team.objects.get(lv_id = g['team_1_id'])
                sms = SMS.objects.create(message = msg,
                                         team = team_obj,
                                         round_id = thisRound['round_number'],
                                         tournament = tourney,
                                         status = u'ready')
                nr_created += 1
            if g['team_2'] is not None:
                msg=self.msg_swiss_team(prevRound,thisRound,g['team_2'],g['team_1'],g['start_time'],g['game_site']['name'],vp_bye) 
                if settings.HOST=="http://api.playwithlv.com":
                    team_obj=Team.objects.get(l_id = g['team_2_id'])
                elif settings.HOST=="https://api.leaguevine.com":
                    team_obj=Team.objects.get(lv_id = g['team_2_id'])
                sms = SMS.objects.create(message = msg,
                                         team = team_obj,
                                         round_id = thisRound['round_number'],
                                         tournament = tourney,
                                         status = u'ready')
                nr_created += 1
        
        return nr_created
            
        
    def msg_swiss_team(self,prevRound,thisRound,team,opp,start_time,field_name,vp_bye):    
        if not prevRound.__contains__('round_number'):
            msg=u'Welcome to Windmill Windup 2012! In Round 1,'
            tomorrow=False
        else:
#            start_time_struct=time.strptime(start_time,"%Y-%m-%dT%H:%M:%S+02:00")
            start_datetime=datetime.strptime(start_time[:-6],"%Y-%m-%dT%H:%M:%S")
            prev_round_datetime = datetime.strptime(prevRound['start_time'][:-6],"%Y-%m-%dT%H:%M:%S")
            if start_datetime.date()>prev_round_datetime.date():
                tomorrow=True
            else:
                tomorrow=False
            msg=u'After a {0} '.format(result_in_swissround(prevRound,team['id']))
            msg += u'in round {0}, '.format(prevRound['round_number'])

        if thisRound['round_number']<9: 
            msg += u'you are now ranked {0}.'.format(ordinal(rank_in_swissround(prevRound,team['id'])))
            msg += u'In round {0}'.format(thisRound['round_number']) + ','
            if opp is None:
                msg += u"you can take a break due to the odd number of teams.You'll score {0} victory points.".format(vp_bye)
            else:
                msg += u"you'll play {0} ".format(opp['name'])
                msg += u"(ranked {0}) ".format(ordinal(rank_in_swissround(prevRound,opp['id'])))            
                msg += u"on {0} ".format(field_name)
                if tomorrow:
                    msg += u'tomorrow '
                msg += u"at {0}.".format(start_datetime.strftime(u"%H:%M"))
            if tomorrow:
                msg += u"Pls hand in today's spirit scores."
        else: # last round
            msg += u'you finish Windmill 2012 in rank {0}, congrats!'.format(rank_in_swissround(prevRound,team['id']))
            msg += u'Please hand in all spirit scores and see you next year!'
        
        return msg
    
    
        
        
class SMS(models.Model):
    objects = SMSManager()
    
    team = models.ForeignKey(Team,blank=True)
    round_id = models.IntegerField(null=True,blank=True)
    # many-to-one relationship between Tournaments and SMS
    tournament = models.ForeignKey(Tournament,blank=True)
    number = models.CharField(max_length=20)
    message = models.CharField(max_length=540) # 3*180 = 540
    length = models.IntegerField(null=True,blank=True)
    
    responseCode = models.IntegerField(null=True,blank=True)
    responseMessage = models.CharField(max_length=100,blank=True)
#    status = models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=50,blank=True)
    createTime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    submitTime = models.DateTimeField(null=True,blank=True)
    sentTime = models.DateTimeField(null=True,blank=True)
    receivedTime = models.DateTimeField(null=True,blank=True)
    

    def __unicode__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.length=len(self.message)
        super(SMS, self).save(*args, **kwargs) # Call the "real" save() method.

