from django.db import models

class Game(models.Model):
    
    # leaguevine game-id
    l_id = models.IntegerField(null=True)
    
    team1_id = models.IntegerField(null=True)
    team2_id = models.IntegerField(null=True)
    
    # totals
    team1_spirit = models.IntegerField(null=True)
    team2_spirit = models.IntegerField(null=True)

    # todo: when teams are filling in the sheets, we will more detailed categories:
    # team1_rules
    # team1_fouls
    # team1_fairmind
    # team1_positive
    # team1_compare
    

    def __unicode__(self):
        return self.l_id

