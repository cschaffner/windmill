from django.conf import settings
from django.db import models
from windmill.tools.wrapper import api_weblink

class Tournament(models.Model):
    # actually a division of Windmill Windup, but in leaguevine
    # every division plays it's own tournament
    
    # id on playwithlv.com
    l_id = models.IntegerField(null=True,blank=True)
    # id on leaguevine.com
    lv_id = models.IntegerField(null=True,blank=True)
    
    # here should be additional properties of the division that are not provided on leaguevine
    name = models.CharField(max_length=50)
    
    def lgv_id(self):
        if settings.HOST=="http://api.playwithlv.com":
            return self.l_id
        else:
            return self.lv_id

    def link(self):
        if self.lgv_id() is None:
            return ""
        else:
            return api_weblink(self.lgv_id())

    
    def nrteams(self):
        return self.teams.count

    def __unicode__(self):
        return self.name

class Team(models.Model):
    
    # id on playwithlv.com
    l_id = models.IntegerField(null=True,blank=True)
    # id on leaguevine.com
    lv_id = models.IntegerField(null=True,blank=True)
    
    # many-to-one relationship between Tournaments and Teams
    tournament = models.ForeignKey(Tournament,null=True,blank=True)

    # now comes all the team data that is not provided by leaguevine:
    name = models.CharField(max_length=50)
    seed = models.IntegerField(null=True,blank=True)
    short_name = models.CharField(max_length=50, null=True,blank=True)
    team_email = models.EmailField(null=True,blank=True)
    contact_name = models.CharField(max_length=200,null=True,blank=True)
    contact_email = models.EmailField(null=True,blank=True)
    sec_contact_name = models.CharField(max_length=200,null=True,blank=True)
    sec_contact_email = models.EmailField(null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    country_code = models.CharField(max_length=2,null=True,blank=True)
    comment = models.TextField(null=True,blank=True)
    mobile1 = models.CharField(max_length=20,null=True,blank=True)
    mobile2 = models.CharField(max_length=20,null=True,blank=True)
    mobile3 = models.CharField(max_length=20,null=True,blank=True)
    mobile4 = models.CharField(max_length=20,null=True,blank=True)
    mobile5 = models.CharField(max_length=20,null=True,blank=True)

    def lgv_id(self):
        if settings.HOST=="http://api.playwithlv.com":
            return self.l_id
        else:
            return self.lv_id
    
    def mobilenr(self):
        # return iterator of available phone numbers 
        for nr in [self.mobile1,self.mobile2,self.mobile3,self.mobile4,self.mobile5]:
            if nr != '':
                yield nr
                
    
    def division(self):
        return self.tournament.name

    def __unicode__(self):
        return self.name
