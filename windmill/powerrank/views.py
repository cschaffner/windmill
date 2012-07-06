from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from windmill.powerrank.models import Tournament, Team, Game
import logging
from pprint import pformat

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


def home(request):
    from numpy import arange        

#    # create a new directory for the output of this routine
#    output_path='/static/output/{0:%Y%m%d_%H%M%S%f}'.format(datetime.now())
#    os_path='{0}{1}'.format(settings.ROOT_PATH,output_path)
#    os.mkdir(os_path)
    
    # make a figure with the rank curves of the top8 teams
    teams=Team.objects.order_by('final_rank')    
    for team in teams:
        strg=team.standing_set.order_by('round').values_list('strength',flat=1)
        str_list=[]
        for el in strg:
            str_list.append(float(el))
        team.str_list=str_list

        swiss_scores=team.standing_set.order_by('round').values_list('swiss_score',flat=1)
        lst=[]
        for i,el in enumerate(swiss_scores,1):
            if el==None:
                break
            lst.append(round(float(el)/i,2))
        team.swiss_scores=lst
        chris_ranks=team.standing_set.order_by('round').values_list('chris_rank',flat=1)
        lst=[]
        for el in chris_ranks:
            if el==None:
                break
            lst.append(float(el))
        team.chris_ranks=lst
        mark_ranks=team.standing_set.order_by('round').values_list('mark_rank',flat=1)
        lst=[]
        for el in mark_ranks:
            if el==None:
                break
            lst.append(float(el))
        team.mark_ranks=lst
        power_ranks=team.standing_set.order_by('round').values_list('power_rank',flat=1)
        team.power_ranks=power_ranks


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
        
    return render_to_response('powerrank.html',{'upsets': upsets,'teams': teams})

def addtournament(request,tournament_id):
    Tournament.objects.add(tournament_id)
    return HttpResponseRedirect('/powerrank/')
