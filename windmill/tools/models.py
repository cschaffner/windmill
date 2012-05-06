from django.db import models
from windmill.tools.wrapper import api_weblink

class Tournament(models.Model):
    # actually a division of Windmill Windup, but in leaguevine
    # every division plays it's own tournament
    
    # leaguevine_id is also used as primary index here
    l_id = models.IntegerField(null=True)
    
    # here should be additional properties of the division that are not provided on leaguevine
    name = models.CharField(max_length=50)
    
    def link(self):
        if self.l_id is None:
            return ""
        else:
            return api_weblink(self.l_id)
    
    def nrteams(self):
        return self.teams.count

    def __unicode__(self):
        return self.name

class Team(models.Model):
    
    # leaguevine_id is used as primary index here as well
    # or not...
    l_id = models.IntegerField(null=True)
    
    # many-to-one relationship between Tournaments and Teams
    tournament = models.ForeignKey(Tournament,null=True)

    # now comes all the team data that is not provided by leaguevine:
    name = models.CharField(max_length=50)
    seed = models.IntegerField(null=True,blank=True)
    short_name = models.CharField(max_length=50, null=True,blank=True)
    team_email = models.EmailField()
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    sec_contact_name = models.CharField(max_length=200)
    sec_contact_email = models.EmailField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    comment = models.TextField()
    mobile1 = models.CharField(max_length=20)
    mobile2 = models.CharField(max_length=20,blank=True)
    mobile3 = models.CharField(max_length=20,blank=True)
    mobile4 = models.CharField(max_length=20,blank=True)
    mobile5 = models.CharField(max_length=20,blank=True)
    
    def mobilenr(self):
        # return iterator of available phone numbers 
        for nr in [self.mobile1,self.mobile2,self.mobile3,self.mobile4,self.mobile5]:
            if nr != '':
                yield nr
                
    
    def division(self):
        return self.tournament.name

    def __unicode__(self):
        return self.name
