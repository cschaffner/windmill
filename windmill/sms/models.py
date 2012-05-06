from django.db import models
from windmill.tools.models import Team 
import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


class Tournament(models.Model):
    l_id = models.IntegerField()
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
                

class SMS(models.Model):
    objects = SMSManager()
    
    team = models.ForeignKey(Team,null=True,blank=True)
    round_id = models.IntegerField()
    # many-to-one relationship between Tournaments and SMS
    tournament = models.ForeignKey(Tournament,null=True,blank=True)
    message = models.CharField(max_length=540,null=True,blank=True) # 3*180 = 540
    status = models.IntegerField()
    createTime = models.DateTimeField()
    submitTime = models.DateTimeField()
    sentTime = models.DateTimeField()
    receivedTime = models.DateTimeField()
    

    def __unicode__(self):
        return str(self.id)

