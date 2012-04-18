from django.db import models

class Game(models.Model):
    
    # leaguevine game-id
    l_id = models.IntegerField(null=True)
    
    team_1_id = models.IntegerField(null=True)
    team_2_id = models.IntegerField(null=True)
    
    team_1_name = models.CharField(max_length=50,null=True)
    team_2_name = models.CharField(max_length=50,null=True)
    
    tournament_id = models.IntegerField(null=True)
    tournament_name = models.CharField(max_length=50,null=True)
    
    start_time = models.DateTimeField(null=True)
    field = models.CharField(max_length=50,null=True)
    
    # totals
    team_1_spirit = models.IntegerField(null=True)
    team_2_spirit = models.IntegerField(null=True)

    # todo: when teams are filling in the sheets, we will more detailed categories:
    # team1_rules
    # team1_fouls
    # team1_fairmind
    # team1_positive
    # team1_compare
    

    def __unicode__(self):
        return str(self.l_id)

