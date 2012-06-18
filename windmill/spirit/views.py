from __future__ import division
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.conf import settings
from windmill.spirit.models import Game, Team
import logging
from pprint import pformat

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


def home(request):
    # refer to admin interface 
    return render_to_response('spirit_added_games.html',{'added': 0})

def update(request):
    # refer to admin interface 
    Team.objects.update_all()
    return render_to_response('spirit_added_games.html',{'added': 0})

    

def addgames(request,tournament_id):
    # add games
    added=Game.objects.addmatches(tournament_id)
    
    return render_to_response('spirit_added_games.html',{'added': added})