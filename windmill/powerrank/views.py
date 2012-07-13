from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from windmill.powerrank.models import Tournament, Team, Game, Tournament_Team
import logging
from pprint import pformat

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')

def home(request):
    tournaments=Tournament.objects.all()
    return render_to_response('power_index.html',{'tournaments': tournaments})

def power(request,tournament_id):
    from numpy import arange
    from windmill.tools.wrapper import ordinal      
    import json

#    # create a new directory for the output of this routine
#    output_path='/static/output/{0:%Y%m%d_%H%M%S%f}'.format(datetime.now())
#    os_path='{0}{1}'.format(settings.ROOT_PATH,output_path)
#    os.mkdir(os_path)
    
    # prepare the data of the teams
    tteams=Tournament_Team.objects.filter(tournament__lv_id=tournament_id).order_by('final_rank','seed')    
    for tteam in tteams:
        str_list=[]
        nr_rounds = tteam.team.standing_set.count()
        for rnd_nr,stand in enumerate(tteam.team.standing_set.order_by('round'),1):
            gm=tteam.team.game_round_nr(tteam.tournament,rnd_nr)
            if gm.team_1==tteam.team:
                opp=gm.team_2
            else:
                opp=gm.team_1
            opp_stand=opp.standing_round_nr(tteam.tournament,rnd_nr)
            opp_prev_stand=opp.standing_round_nr(tteam.tournament,rnd_nr-1)
            
            if rnd_nr==1:
                st=tteam.team.standing_round_nr(tteam.tournament,0)
                descr="seed: {0}<br>".format(st.chris_rank)
                descr += "R1: {1} vs {2}<br>".format(rnd_nr,gm.team_1.name.encode('ascii','xmlcharrefreplace'),gm.team_2.name.encode('ascii','xmlcharrefreplace'))
                descr += "score: {0} - {1}, margin: {2}<br>".format(gm.team_1_score,gm.team_2_score,gm.team_1_score-gm.team_2_score)
                descr += "expected margin: after R1 {0:4.2f}, after R{2} {1:4.2f}<br>strength".format(gm.pred_margin_current, gm.pred_margin_overall,nr_rounds)
                descr += ": {0:4.2f} ({1})<br>".format(stand.strength,ordinal(stand.power_rank))          
                descr += "opponent's strength"
                descr += ": {0:4.2f} ({1})".format(opp_stand.strength,ordinal(opp_stand.power_rank))
            else:
                if gm.team_1==tteam.team:
                    gm.pred_margin_prev = prev_strength-opp_prev_stand.strength
                else:
                    gm.pred_margin_prev = opp_prev_stand.strength - prev_strength

                descr = "R{0}: {1} vs. {2}<br>".format(rnd_nr,gm.team_1.name.encode('ascii','xmlcharrefreplace'),gm.team_2.name.encode('ascii','xmlcharrefreplace'))
                descr += "score: {0} - {1}, margin: {2}<br>".format(gm.team_1_score,gm.team_2_score,gm.team_1_score-gm.team_2_score)
                descr += "expected margin: before R{0} {1:4.2f},<br> after R{0} {2:4.2f}, ".format(rnd_nr,gm.pred_margin_prev,gm.pred_margin_current)
                descr += "ofter R{0} {1:4.2f}<br>".format(nr_rounds,gm.pred_margin_overall)
                if prev_strength <= stand.strength:
                    descr += "strength increased "
                else:
                    descr += "strength decreased "
                descr += "from {0:4.2f} ({1}) to {2:4.2f} ({3})<br>".format(prev_strength,ordinal(prev_rank),stand.strength,ordinal(stand.power_rank))
                if opp_prev_stand.strength <= opp_stand.strength:
                    descr += "opponent's strength increased "
                else: 
                    descr += "opponent's strength decreased "
                descr += "from {0:4.2f} ({1}) to {2:4.2f} ({3})".format(opp_prev_stand.strength,
                            ordinal(opp_prev_stand.power_rank),opp_stand.strength,ordinal(opp_stand.power_rank))
            prev_strength=stand.strength
            prev_rank=stand.power_rank
            jsn={"y": round(float(stand.strength),2), "rank": "{0}".format(ordinal(stand.power_rank)), "name": json.dumps(tteam.team.name), "text": descr}
#            logger.info(pformat(jsn))
            str_list.append(jsn)
        tteam.str_list=str_list

        swiss_scores=tteam.team.standing_set.order_by('round').values_list('swiss_score',flat=1)
        lst=[]
        for i,el in enumerate(swiss_scores,1):
            if el==None:
                break
            lst.append(round(float(el)/i,2))
        tteam.swiss_scores=lst
        chris_ranks=tteam.team.standing_set.order_by('round').values_list('chris_rank',flat=1)
        lst=[]
        for el in chris_ranks:
            if el==None:
                break
            lst.append(float(el))
        tteam.chris_ranks=lst
        mark_ranks=tteam.team.standing_set.order_by('round').values_list('mark_rank',flat=1)
        lst=[]
        for el in mark_ranks:
            if el==None:
                break
            lst.append(float(el))
        tteam.mark_ranks=lst
        power_ranks=tteam.team.standing_set.order_by('round').values_list('power_rank',flat=1)
        tteam.power_ranks=power_ranks


    upsets=Game.objects.filter(round__tournament__lv_id=tournament_id).order_by('-upset_current')[:10]
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
        
    return render_to_response('powerrank.html',{'upsets': upsets,'teams': tteams})

def addtournament(request,tournament_id):
    Tournament.objects.add(tournament_id)
    return HttpResponseRedirect('/powerrank/')
