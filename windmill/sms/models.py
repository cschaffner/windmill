from django.db import models
from windmill.tools.models import Team 

class Tournament(models.Model):
    l_id = models.IntegerField()
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.name)


class SMS(models.Model):
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

