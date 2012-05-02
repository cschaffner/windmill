from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.conf import settings
from windmill.tools.wrapper import *
from windmill.spirit.models import Game
import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


def home(request):
    return render_to_response('spirit.html',{'Games': Game.objects.all})

def addgames(request,tournament_id):
    # retrieve all games from tournament
    games=api_gamesbytournament(tournament_id)
    logger.info(games)
    # import all games from tournament in local db
    for g in games['objects']:
        gm,created=Game.objects.get_or_create(l_id=g['id'])
        if g['team_1_id'] is not None:            
            gm.team_1_id=g['team_1_id']
            gm.team_1_name=g['team_1']['name']
        if g['team_2_id'] is not None:            
            gm.team_2_id=g['team_2_id']
            gm.team_2_name=g['team_2']['name']
        gm.tournament_id = g['tournament']['id']
        gm.tournament_name = g['tournament']['name']
        gm.start_time = g['start_time']
        # gm.field = g['field']
        logger.info('added game {0} - {1}'.format(g['team_1_id'],g['team_2_id']))
        gm.save()
    
    return render_to_response('spirit.html',{'Games': Game.objects.all})