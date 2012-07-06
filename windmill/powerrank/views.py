from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from windmill.powerrank.models import Tournament, Game
import logging
from pprint import pformat

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


def home(request):
    upsets=Game.objects.filter(upset_current__gte=15).order_by('-upset_current')
    # upgrade team information with ranks
    for gm in upsets:        
        gm.margin=gm.team_1_score - gm.team_2_score
        gm.team_1.chris_rank=gm.team_1.standing_set.get(round=gm.round).chris_rank        
        gm.team_1.mark_rank=gm.team_1.standing_set.get(round=gm.round).mark_rank        
        gm.team_1.strength=gm.team_1.standing_set.get(round=gm.round).strength        
#        gm.team_1.final_rank=gm.team_1.standing_set.get(round=gm.round).chris_rank        
        gm.team_2.chris_rank=gm.team_2.standing_set.get(round=gm.round).chris_rank        
        gm.team_2.mark_rank=gm.team_2.standing_set.get(round=gm.round).mark_rank        
        gm.team_2.strength=gm.team_2.standing_set.get(round=gm.round).strength        
#        gm.team_1.final_rank=gm.team_1.standing_set.get(round=gm.round).chris_rank        
        
    return render_to_response('powerrank.html',{'upsets': upsets})

def addtournament(request,tournament_id):
    Tournament.objects.add(tournament_id)
    return HttpResponseRedirect('/powerrank/')
