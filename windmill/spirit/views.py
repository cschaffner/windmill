from __future__ import division
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.conf import settings
from windmill.spirit.models import Game
import logging
from pprint import pformat

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


def home(request):
    # calculate spirit scores
    
    # store them in a nested dictionary    
    s={}
    
    # loop over all games and fill in spirit scores by team
    for g in Game.objects.all():
        if not s.has_key(g.tournament_id):
            s[g.tournament_id]={"name": g.tournament_name, "teams": {}}            
        # treat first team
        if not s[g.tournament_id]['teams'].has_key(g.team_1_id):
            s[g.tournament_id]['teams'][g.team_1_id]={"name": g.team_1_name}
        if s[g.tournament_id]['teams'][g.team_1_id].has_key('received'):
            s[g.tournament_id]['teams'][g.team_1_id]['received'].append(g.team_1_spirit)
        else:
            s[g.tournament_id]['teams'][g.team_1_id]['received']=[g.team_1_spirit]
        if s[g.tournament_id]['teams'][g.team_1_id].has_key('given'):
            s[g.tournament_id]['teams'][g.team_1_id]['given'].append(g.team_2_spirit)
        else:
            s[g.tournament_id]['teams'][g.team_1_id]['given']=[g.team_2_spirit]
        # treat second team
        if not s[g.tournament_id]['teams'].has_key(g.team_2_id):
            s[g.tournament_id]['teams'][g.team_2_id]={"name": g.team_2_name}
        if s[g.tournament_id]['teams'][g.team_2_id].has_key('received'):
            s[g.tournament_id]['teams'][g.team_2_id]['received'].append(g.team_2_spirit)
        else:
            s[g.tournament_id]['teams'][g.team_2_id]['received']=[g.team_2_spirit]
        if s[g.tournament_id]['teams'][g.team_2_id].has_key('given'):
            s[g.tournament_id]['teams'][g.team_2_id]['given'].append(g.team_1_spirit)
        else:
            s[g.tournament_id]['teams'][g.team_2_id]['given']=[g.team_1_spirit]

    logger.info(pformat(s))

    for div_id,div in s.items():
        for team_id, team in div['teams'].items():
            team['nr_given'],team['avg_given']=compute(team['given'])
            team['nr_received'],team['avg_received']=compute(team['received'])
    
    logger.info(pformat(s))
            
    
    
    # 
    return render_to_response('spirit.html',{'Spirit': s})

    

def addgames(request,tournament_id):
    # add games
    added=Game.objects.addmatches(tournament_id)
    
    return render_to_response('added_games.html',{'added': added})