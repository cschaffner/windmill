from django.db import models
from windmill.tools.models import Team, Tournament
import logging
from datetime import datetime
from windmill.tools.wrapper import *
# Import the SmsCity Library which will send the message to our server
from SmsCity import SmsCity
from random import getrandbits
import unicodedata


# Get an instance of a logger
logger = logging.getLogger('windmill.sms')



class SMSManager(models.Manager):
    def change_status_to_sent(self):
        SendList = SMS.objects.filter(status=u'ready')
        for sms in SendList:
            sms.status="sent"
            sms.save()
        return 
    
    def sendSmsCity(self):
        # sends all SMS with status 1 to SmsCity
        
        SendList = SMS.objects.filter(status=u'ready')

#        if SendList.count()>1:
#            logger.error('we do not want to send too much for now')
#            raise
        
        counter=0
        for sms in SendList:
            # Set the SMScity username and password, and create an instance of the SmsCity class
            smsApi = SmsCity('windmill', '2smscity')
            
            # Set the sender, could be an number (16 numbers) or letters (11 characters)
            smsApi.setSender('WW_2012')
            
            # Add the destination mobile number.
            # This method can be called several times to add have more then one recipient for the same message
            smsApi.setDestination(sms.number)
            
            if len(smsApi.destination) > 1:
                raise Exception('sms has more than one destination number, we had that before...')
            
            # Set an reference
    #        ref=getrandbits(63)
            smsApi.setReference(sms.id)
            
            # make sure there are no special symbols in the message
            # convert it to ASCII
            msg_ascii = unicodedata.normalize('NFKD', sms.message).encode('ascii','ignore')

            logger.info('sending sms "{0}" to {1}'.format(msg_ascii,sms.number))
            # Send the message to the destination(s)
            smsApi.sendSms(msg_ascii)
            counter += 1
            
            # When using in the console, it will show you what the response was from our server
            logger.info('Response: {0}'.format(smsApi.getResponseCode()))
            logger.info('{0}'.format(smsApi.getResponseMessage()))
            logger.info('{0}'.format(smsApi.getCreditBalance()))
    
            sms.submitTime = datetime.now()
            sms.responseCode=smsApi.getResponseCode()
            sms.responseMessage=smsApi.getResponseMessage()
            sms.status="Sent"
            
            sms.save()
            
            if counter>=30:
                break
        
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
    
    def sendIndividualSMS(self,message,nr):
        # send SMS with message
        # to an individual number
        
        sms = SMS.objects.create(message=message, number=nr, status=u'ready')
        logger.info('created 1 individual SMS to nr: {0}'.format(nr))
        return 1

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

    def bracket_round(self,brackets,swiss,selround,tournament):
        """
        Brackets:
                
                    
        // After a 13-12 win in the exciting final, you are the champion of Windmill 2010. Congratulations!"
        // After a 11-18 loss in the final, you are vice-champion of Windmill 2010. Congratulations!"
        """
    
        lastSwissRound={}
        for r in swiss['objects']:
            if r['round_number']==5:
                lastSwissRound=r

        # retrieve the tournament from the database
        # assumes that those tournaments already exist there
        if settings.HOST=="http://api.playwithlv.com":
            tourney=Tournament.objects.get(l_id = tournament['id'])
        elif settings.HOST=="https://api.leaguevine.com":
            tourney=Tournament.objects.get(lv_id = tournament['id'])
        
        nr_created=0
        
        # case distinction between quarters, semi, finals and big final
        if selround=='QF':
            # retrieve the biggest playoff bracket
            for br in brackets['objects']:
                if br['number_of_rounds']==3:
                    for r in br['rounds']:
                        # retrieve the first round, that's the quarter finals
                        if r['round_number']==2:
                            quarters=r
            for g in quarters['games']:
                if g['team_1'] is not None:
                    msg=self.msg_quarters_team(lastSwissRound,quarters,g['team_1'],g['team_2'],g['start_time'],self.gsite(g)) 
                    nr_created += self.create_sms_team(msg,g['team_1_id'],'QF',tourney)
                if g['team_2'] is not None:
                    msg=self.msg_quarters_team(lastSwissRound,quarters,g['team_2'],g['team_1'],g['start_time'],self.gsite(g)) 
                    nr_created += self.create_sms_team(msg,g['team_2_id'],'QF',tourney)                                    
        elif selround=='SF':
            # retrieve relevant rounds
            for br in brackets['objects']:
                if br['number_of_rounds']==3:  # get the biggest playoff bracket
                    for r in br['rounds']:
                        # retrieve the first round, that's the quarter finals
                        if r['round_number']==2:
                            quarters=r
                        # retrieve the second round, that's one half of the semi finals
                        if r['round_number']==1:
                            semis1=r
                elif br['number_of_rounds']==2: # that's the loser's playoffs
                    for r in br['rounds']:
                        if r['round_number']==1: 
                            semis2=r
                                                    
            for g in semis1['games']+semis2['games']: # check if this concatenation of arrays works
                if g['team_1'] is not None:
                    msg=self.msg_semis_team(quarters,g['team_1'],g['team_2'],g['start_time'],self.gsite(g))                    
                    nr_created += self.create_sms_team(msg,g['team_1_id'],'SF',tourney)
                if g['team_2'] is not None:
                    msg=self.msg_semis_team(quarters,g['team_2'],g['team_1'],g['start_time'],self.gsite(g)) 
                    nr_created += self.create_sms_team(msg,g['team_2_id'],'SF',tourney)                                    
        elif selround=='F':
            # retrieve relevant rounds
            for br in brackets['objects']:
                if br['number_of_rounds']==3:  # get the biggest playoff bracket
                    for r in br['rounds']:
                        # retrieve the first round, that's the Big Final
                        if r['round_number']==0:
                            final_12=r
                        # retrieve the second round, that's one half of the semi finals
                        if r['round_number']==1:
                            semis1=r
                elif br['number_of_rounds']==2: # that's the loser's playoffs
                    for r in br['rounds']:
                        if r['round_number']==1: 
                            semis2=r
                        if r['round_number']==0: 
                            final_56=r
                elif br['number_of_rounds']==1 and br['name']=='bronze game':
                    final_34 = br['rounds'][0]
                elif br['number_of_rounds']==1 and br['name']=='game for 7-8':
                    final_78 = br['rounds'][0]
            semis={} # set up a collection of semi rounds
            semis['start_time']=semis1['games'][0]['start_time']  # set the start_time of all semis to the start_time of the first game of semis1 (that's pretty arbitrary)
            semis['games']=semis1['games']+semis2['games']               
                                                                
            for idx,g in enumerate(final_12['games']+final_34['games']+final_56['games']+final_78['games']):
                if g['team_1'] is not None:
                    msg=self.msg_finals_team(semis,g['team_1'],g['team_2'],g['start_time'],self.gsite(g),(idx*2)+1)                     
                    nr_created += self.create_sms_team(msg,g['team_1_id'],'F',tourney)
                if g['team_2'] is not None:
                    msg=self.msg_finals_team(semis,g['team_2'],g['team_1'],g['start_time'],self.gsite(g),(idx*2)+1)                     
                    nr_created += self.create_sms_team(msg,g['team_2_id'],'F',tourney)                                    
        elif selround=='afterF':
            # retrieve relevant rounds
            for br in brackets['objects']:
                if br['number_of_rounds']==3:  # get the biggest playoff bracket
                    for r in br['rounds']:
                        # retrieve the first round, that's the Big Final
                        if r['round_number']==0:
                            final_12=r
                        # retrieve the second round, that's one half of the semi finals
                        if r['round_number']==1:
                            semis1=r
                elif br['number_of_rounds']==2: # that's the loser's playoffs
                    for r in br['rounds']:
                        if r['round_number']==1: 
                            semis2=r
                        if r['round_number']==0: 
                            final_56=r
                elif br['number_of_rounds']==1 and br['name']=='bronze game':
                    final_34 = br['rounds'][0]
                elif br['number_of_rounds']==1 and br['name']=='game for 7-8':
                    final_78 = br['rounds'][0]
                    
            finals={} # set up a collection of semi rounds
            finals['games']=final_12['games']+final_34['games']+final_56['games']+final_78['games']               

            for idx,g in enumerate(finals['games']):
                if g['team_1'] is not None:
                    msg=self.msg_after_finals_team(finals,g['team_1'],(idx*2)+1)                     
                    nr_created += self.create_sms_team(msg,g['team_1_id'],'aftF',tourney)
                if g['team_2'] is not None:
                    msg=self.msg_after_finals_team(finals,g['team_2'],(idx*2)+1)                     
                    nr_created += self.create_sms_team(msg,g['team_2_id'],'aftF',tourney)                                    
        
        return nr_created

    def msg_after_finals_team(self,finals,team,for_place):
        # After a 15-2 loss in the final game, you finish Windmill 2010 in place 1. Congratulations!
        # Please hand in today's spirit scores and see you next year!
        
        result_txt=result_in_swissround(finals,team['id'])
        place=for_place
        if result_txt[-4:]=='loss':
            place=for_place+1

        msg=u'After a {0} '.format(result_txt)
        msg += u'in the final game, '
        msg += u"{0} ".format(self.sname(team))
        
        msg += u'finishes Windmill 2012 as {0}, congrats! '.format(ordinal(place))
        msg += u'Please hand in all spirit scores and see you next year!'
        
        return msg

        
    def msg_finals_team(self,semis,team,opp,start_time,field_name,for_place):
        # After a 15-2 loss in the semi finals, 
        # you'll play for 9th against "Ultimate Kaese" (Swiss-ranked 13th) on Field 1 at 12:30.
            
        start_datetime=datetime.strptime(start_time[:-6],"%Y-%m-%dT%H:%M:%S")
        prev_round_datetime = datetime.strptime(semis['games'][0]['start_time'][:-6],"%Y-%m-%dT%H:%M:%S")
        if start_datetime.date()>prev_round_datetime.date():
            tomorrow=True
        else:
            tomorrow=False
        msg=u'After a {0} '.format(result_in_swissround(semis,team['id']))
        msg += u'in the semi finals, '
        msg += u"{0} ".format(self.sname(team))

        msg += u'will play for {0} place '.format(ordinal(for_place)) 
        msg += u'against {0} '.format(self.sname(opp))
        msg += u"on {0} ".format(field_name)
        if tomorrow:
            msg += u'tomorrow '
        msg += u"at {0}.".format(start_datetime.strftime(u"%H:%M"))
        if tomorrow:
            msg += u"Pls hand in today's spirit scores."
        
        return msg

        
    def msg_semis_team(self,quarters,team,opp,start_time,field_name):
        # After a 15-2 loss in the quarter finals, you'll play the next rounds against
        # "Ultimate Kaese" on Field 1 at 12:30.
            
        start_datetime=datetime.strptime(start_time[:-6],"%Y-%m-%dT%H:%M:%S")
        prev_round_datetime = datetime.strptime(quarters['games'][0]['start_time'][:-6],"%Y-%m-%dT%H:%M:%S")
        if start_datetime.date()>prev_round_datetime.date():
            tomorrow=True
        else:
            tomorrow=False
        msg=u'After a {0} '.format(result_in_swissround(quarters,team['id']))
        msg += u'in the quarter finals, '
        msg += u"{0} ".format(self.sname(team))

        msg += u'will play {0} '.format(self.sname(opp))
        msg += u"on {0} ".format(field_name)
        if tomorrow:
            msg += u'tomorrow '
        msg += u"at {0}.".format(start_datetime.strftime(u"%H:%M"))
        if tomorrow:
            msg += u"Pls hand in today's spirit scores."
        
        return msg

    
    def msg_quarters_team(self,lastswiss,quarters,team,opp,start_time,field_name):
        # After a 15-10 win in round 5, your final rank after Swissdraw is 25th. You will thus play for rank 1 to 8.
        # In the quarter finals, you'll play CamboCakes (ranked 5th) on Field 10. Pls handin today's spirit scores.
            
        start_datetime=datetime.strptime(start_time[:-6],"%Y-%m-%dT%H:%M:%S")
        prev_round_datetime = datetime.strptime(lastswiss['start_time'][:-6],"%Y-%m-%dT%H:%M:%S")
        if start_datetime.date()>prev_round_datetime.date():
            tomorrow=True
        else:
            tomorrow=False
        msg=u'After a {0} '.format(result_in_swissround(lastswiss,team['id']))
        msg += u'in round {0}, '.format(lastswiss['round_number'])
        msg += u"{0} ".format(self.sname(team))

        msg += u'is now ranked {0}. You will thus play for rank 1 to 8 in playoffs.'.format(rank_in_swissround(lastswiss,team['id']))
        msg += u"In the quarter finals, you'll play {0} ".format(self.sname(opp))
        msg += u"(ranked {0}) ".format(rank_in_swissround(lastswiss,opp['id']))            
        msg += u"on {0} ".format(field_name)
        if tomorrow:
            msg += u'tomorrow '
        msg += u"at {0}.".format(start_datetime.strftime(u"%H:%M"))
        if tomorrow:
            msg += u"Pls hand in today's spirit scores."
        
        return msg

    
    def swiss_round(self,prevRound,thisRound,round_nr,tournament):
    
#        prevRound={}
#        for r in swiss['objects']:
#            if round_nr > 1 and r['round_number']==(round_nr-1):
#                prevRound=r
#            elif r['round_number']==round_nr:
#                thisRound=r
        if round_nr==9:
            thisRound={}
            thisRound['round_number']=9
            # set games equal to last round's games so that below, we go through all teams and create the final sms
            thisRound['games']=prevRound['games']
            
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
                nr_created += self.create_sms_team(msg,g['team_1_id'],thisRound['round_number'],tourney)
            if g['team_2'] is not None:
                msg=self.msg_swiss_team(prevRound,thisRound,g['team_2'],g['team_1'],g['start_time'],g['game_site']['name'],vp_bye) 
                nr_created += self.create_sms_team(msg,g['team_2_id'],thisRound['round_number'],tourney)

        return nr_created
            
        
    def msg_swiss_team(self,prevRound,thisRound,team,opp,start_time,field_name,vp_bye):
            
        if not prevRound.__contains__('round_number'):
            start_datetime=datetime.strptime(start_time[:-6],"%Y-%m-%dT%H:%M:%S")
            prev_round_datetime = datetime.now()
            if start_datetime.date()>prev_round_datetime.date():
                tomorrow=True
            else:
                tomorrow=False

            msg=u'Welcome to Windmill Windup 2012! In Round 1, {0} '.format(self.sname(team))
            if opp is None:
                msg += u"can take a break due to the odd number of teams.You'll score {0} victory points.".format(vp_bye)
            else:
                msg += u"will play {0} ".format(self.sname(opp))
                msg += u"on {0} ".format(field_name)
                if tomorrow:
                    msg += u'tomorrow '
                msg += u"at {0}.".format(start_datetime.strftime(u"%H:%M"))
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
            msg += u'{0} '.format(self.sname(team))

            if thisRound['round_number']<9: 
                msg += u'is now ranked {0}.'.format(rank_in_swissround(prevRound,team['id']))
                msg += u'In round {0}'.format(thisRound['round_number']) + ','
                if opp is None:
                    msg += u"you can take a break due to the odd number of teams.You'll score {0} victory points.".format(vp_bye)
                else:
                    msg += u"you'll play {0} ".format(self.sname(opp))
                    msg += u"(ranked {0}) ".format(rank_in_swissround(prevRound,opp['id']))            
                    msg += u"on {0} ".format(field_name)
                    if tomorrow:
                        msg += u'tomorrow '
                    msg += u"at {0}.".format(start_datetime.strftime(u"%H:%M"))
                if tomorrow:
                    msg += u"Please hand in today's spirit scores."
            else: # last round
                msg += u'finishes Windmill 2012 as {0}, congrats! '.format(rank_in_swissround(prevRound,team['id']))
                msg += u'Please hand in all spirit scores and see you next year!'
        
        return msg
    
    def sname(self,team):
        # returns the short name if avaible
        # returns normal name otherwise
        if team.has_key('short_name'):
            return team['short_name']
        else:
            return team['name']

    def create_sms_team(self,msg,team_id,round_id,tourney):
        # creates SMS for all phone numbers of the team
        if settings.HOST=="http://api.playwithlv.com":
            team_obj=Team.objects.get(l_id = team_id)
        elif settings.HOST=="https://api.leaguevine.com":
            team_obj=Team.objects.get(lv_id = team_id)                    
        
        # make sure there are no special symbols in the message
        # convert it to ASCII
        msg_ascii = unicodedata.normalize('NFKD', msg).encode('ascii','ignore')
        
        nr_created=0
        for nr in team_obj.mobilenr():
            sms = SMS.objects.create(message = msg_ascii,
                                     number = nr,
                                     team = team_obj,
                                     round_id = round_id,
                                     tournament = tourney,
                                     status = u'ready')
            nr_created += 1            
        return nr_created
    
    def gsite(self,game):
        if game['game_site']!=None:
            return game['game_site']['name']
        else:
            logger.error('no game site found in game id {0}'.format(game['id']))
            return '?'
        
class SMS(models.Model):
    objects = SMSManager()
    
    team = models.ForeignKey(Team,blank=True,null=True,default=None)
    round_id = models.CharField(max_length=5,null=True,blank=True)
    # many-to-one relationship between Tournaments and SMS
    tournament = models.ForeignKey(Tournament,blank=True,null=True,default=None)
    number = models.CharField(max_length=20)
    message = models.CharField(max_length=540) # 3*180 = 540
    length = models.IntegerField(null=True,blank=True)
    
    responseCode = models.IntegerField(null=True,blank=True)
    responseMessage = models.CharField(max_length=100,blank=True,null=True)
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


class SMSOverview(SMS):
    class Meta:
        proxy = True    