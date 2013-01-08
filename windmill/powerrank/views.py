from __future__ import division
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from windmill.powerrank.models import Tournament, Team, Game, Tournament_Team, Round
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
        power_rank_list=[]
        chris_rank_list=[]
        mark_rank_list=[]
        swiss_scores_list=[]
        nr_rounds = tteam.team.standing_set.count()
        for rnd_nr,stand in enumerate(tteam.team.standing_set.order_by('round'),1):
            gm=tteam.team.game_round_nr(tteam.tournament,rnd_nr)
            
            if gm==None:
                # strength description
                descr = "<ul><li>did not play in this round</li>"
                if prev_strength < stand.strength:
                    descr += "<li>strength increased "
                elif prev_strength > stand.strength:
                    descr += "<li>strength decreased "
                else:
                    descr += "<li>strength stayed "
                descr += "from {0:4.2f} ({1}) to {2:4.2f} ({3})".format(prev_strength,ordinal(prev_rank),stand.strength,ordinal(stand.power_rank))
            else:
                if gm.team_1==tteam.team:
                    opp=gm.team_2
                else:
                    opp=gm.team_1
                opp_stand=opp.standing_round_nr(tteam.tournament,rnd_nr)
                opp_prev_stand=opp.standing_round_nr(tteam.tournament,rnd_nr-1)
                
                if rnd_nr==1:
                    st=tteam.team.standing_round_nr(tteam.tournament,0)
                    # power-description
                    descr="<ul><li>seed: {0}".format(st.chris_rank)
                    descr += "<li>R1: {1} vs {2}<br>".format(rnd_nr,gm.team_1.name.encode('ascii','xmlcharrefreplace'),gm.team_2.name.encode('ascii','xmlcharrefreplace'))
                    descr += "score: {0} - {1}, margin: {2}<br>".format(gm.team_1_score,gm.team_2_score,gm.team_1_score-gm.team_2_score)
                    descr += "expected margin: after R1: {0:4.2f}, after R{2}: {1:4.2f}<li>strength".format(gm.pred_margin_current, gm.pred_margin_overall,nr_rounds)
                    descr += ": {0:4.2f} ({1})".format(stand.strength,ordinal(stand.power_rank))          
                    descr += "<li>opponent's strength"
                    descr += ": {0:4.2f} ({1})</ul>".format(opp_stand.strength,ordinal(opp_stand.power_rank))
                    # swisspoint-description
                    des="<ul><li>seed: {0}".format(st.chris_rank)
                    des += "<li>R1: {1} vs {2}<br>".format(rnd_nr,gm.team_1.name.encode('ascii','xmlcharrefreplace'),gm.team_2.name.encode('ascii','xmlcharrefreplace'))
                    des += "score: {0} - {1}, margin: {2}<br>".format(gm.team_1_score,gm.team_2_score,gm.team_1_score-gm.team_2_score)
                    des += "<li>swiss points: {0} ({1})".format(stand.swiss_score,ordinal(stand.chris_rank))
                    des += "<li>opponent's swiss points: {0} ({1})</ul>".format(opp_stand.swiss_score,ordinal(opp_stand.chris_rank))
                else:
                    if gm.team_1==tteam.team:
                        gm.pred_margin_prev = prev_strength-opp_prev_stand.strength
                    else:
                        gm.pred_margin_prev = opp_prev_stand.strength - prev_strength
                    # strength description
                    descr = "<ul><li>R{0}: {1} vs. {2}<br>".format(rnd_nr,gm.team_1.name.encode('ascii','xmlcharrefreplace'),gm.team_2.name.encode('ascii','xmlcharrefreplace'))
                    descr += "score: {0} - {1}, margin: {2}<br>".format(gm.team_1_score,gm.team_2_score,gm.team_1_score-gm.team_2_score)
                    descr += "expected margin: before R{0}: {1:4.2f},<br> after R{0}: {2:4.2f}".format(rnd_nr,gm.pred_margin_prev,gm.pred_margin_current)
                    if rnd_nr < nr_rounds:
                        descr += ", after R{0}: {1:4.2f}".format(nr_rounds,gm.pred_margin_overall)
                    if prev_strength < stand.strength:
                        descr += "<li>strength increased "
                    elif prev_strength > stand.strength:
                        descr += "<li>strength decreased "
                    else:
                        descr += "<li>strength stayed "
                    descr += "from {0:4.2f} ({1}) to {2:4.2f} ({3})".format(prev_strength,ordinal(prev_rank),stand.strength,ordinal(stand.power_rank))
                    if opp_prev_stand.strength <= opp_stand.strength:
                        descr += "<li>opponent's strength increased "
                    else: 
                        descr += "<li>opponent's strength decreased "
                    descr += "from {0:4.2f} ({1}) to {2:4.2f} ({3})".format(opp_prev_stand.strength,
                                ordinal(opp_prev_stand.power_rank),opp_stand.strength,ordinal(opp_stand.power_rank))
                    # swiss points description
                    if stand.swiss_score != None:
                        des = "<ul><li>R{0}: {1} vs. {2}<br>".format(rnd_nr,gm.team_1.name.encode('ascii','xmlcharrefreplace'),gm.team_2.name.encode('ascii','xmlcharrefreplace'))
                        des += "score: {0} - {1}, margin: {2}<br>".format(gm.team_1_score,gm.team_2_score,gm.team_1_score-gm.team_2_score)
                        if prev_swiss_score < stand.swiss_score/rnd_nr:
                            des += "<li>average swiss score increased "
                        elif prev_swiss_score > stand.swiss_score/rnd_nr:
                            des += "<li>average swiss score decreased "
                        else:
                            des += "<li>average swiss score stayed "                    
                        des += "from {0:4.2f} ({1}) to {2:4.2f} ({3})".format(prev_swiss_score,ordinal(prev_chris_rank),stand.swiss_score/rnd_nr,ordinal(stand.chris_rank))
                        if opp_prev_stand.swiss_score/(rnd_nr-1) <= opp_stand.swiss_score/rnd_nr:
                            des += "<li>average opponent's swiss score increased "
                        else:
                            des += "<li>average opponent's swiss score decreased "
                        des += "from {0:4.2f} ({1}) to {2:4.2f} ({3})".format(opp_prev_stand.swiss_score/(rnd_nr-1),
                                    ordinal(opp_prev_stand.chris_rank),opp_stand.swiss_score/rnd_nr,ordinal(opp_stand.chris_rank))
            
            prev_strength=stand.strength
            prev_rank=stand.power_rank
            jsn={"y": round(float(stand.strength),2), "rank": "{0}".format(ordinal(stand.power_rank)), "name": json.dumps(tteam.team.name), "text": descr}
            str_list.append(jsn)
            jsn={"y": stand.power_rank, "rank": "{0}".format(ordinal(stand.power_rank)), "name": json.dumps(tteam.team.name), "text": descr}
            power_rank_list.append(jsn)
            if stand.swiss_score != None:
                prev_swiss_score=stand.swiss_score/rnd_nr
                prev_chris_rank=stand.chris_rank
                jsn={"y": stand.chris_rank, "name": json.dumps(tteam.team.name), "text": des}
                chris_rank_list.append(jsn)
                jsn={"y": stand.mark_rank, "name": json.dumps(tteam.team.name), "text": des}
                mark_rank_list.append(jsn)
                jsn={"y": round(float(stand.swiss_score)/rnd_nr,2), "rank": "{0}".format(ordinal(stand.chris_rank)), "name": json.dumps(tteam.team.name), "text": des}
                swiss_scores_list.append(jsn)
            
        tteam.str_list=str_list
        tteam.power_ranks=power_rank_list
        tteam.chris_ranks=chris_rank_list
        tteam.mark_ranks=mark_rank_list        
        tteam.swiss_scores=swiss_scores_list

#        swiss_scores=tteam.team.standing_set.order_by('round').values_list('swiss_score',flat=1)
#        lst=[]
#        for i,el in enumerate(swiss_scores,1):
#            if el==None:
#                break
#            lst.append(round(float(el)/i,2))
#        tteam.swiss_scores=lst
#        chris_ranks=tteam.team.standing_set.order_by('round').values_list('chris_rank',flat=1)
#        lst=[]
#        for el in chris_ranks:
#            if el==None:
#                break
#            lst.append(float(el))
#        tteam.chris_ranks=lst
#        mark_ranks=tteam.team.standing_set.order_by('round').values_list('mark_rank',flat=1)
#        lst=[]
#        for el in mark_ranks:
#            if el==None:
#                break
#            lst.append(float(el))
#        tteam.mark_ranks=lst
#        power_ranks=tteam.team.standing_set.order_by('round').values_list('power_rank',flat=1)
#        tteam.power_ranks=power_ranks


    finalround=Round.objects.filter(tournament__lv_id=tournament_id).order_by('-round_number')[0]
    upsets=Game.objects.filter(round__tournament__lv_id=tournament_id).order_by('-upset_overall')
    # define an empty class to hold the upset and prediction stats
    class Stat():
        pass
    stat=Stat()
    stat.nr_games=0
    stat.nr_games_predict=0
    stat.nr_corwin_predict=0
    stat.nr_corwin_overall=0    
    # upgrade team information with ranks
    for gm in upsets:
        stat.nr_games += 1
        if gm.team_1_score > gm.team_2_score and gm.team_1.standing_set.get(round=finalround).strength > gm.team_2.standing_set.get(round=finalround).strength:
            stat.nr_corwin_overall += 1
        elif gm.team_1_score < gm.team_2_score and gm.team_1.standing_set.get(round=finalround).strength < gm.team_2.standing_set.get(round=finalround).strength:
            stat.nr_corwin_overall += 1   
        if gm.round.round_number > 1:
            stat.nr_games_predict += 1
            # get strengths of teams from previous round
            prev_strength_1=gm.team_1.standing_round_nr(gm.round.tournament,gm.round.round_number-1).strength
            prev_strength_2=gm.team_2.standing_round_nr(gm.round.tournament,gm.round.round_number-1).strength
            # count if the winner was correctly predicted at that point
            if gm.team_1_score > gm.team_2_score and prev_strength_1 > prev_strength_2:
                stat.nr_corwin_predict += 1
            elif gm.team_1_score < gm.team_2_score and prev_strength_1 < prev_strength_2:
                stat.nr_corwin_predict += 1
        gm.margin=gm.team_1_score - gm.team_2_score
        gm.team_1.chris_rank=gm.team_1.standing_set.get(round=gm.round).chris_rank        
        gm.team_1.mark_rank=gm.team_1.standing_set.get(round=gm.round).mark_rank        
        gm.team_1.cur_strength=gm.team_1.standing_set.get(round=gm.round).strength  
        gm.team_1.final_strength=gm.team_1.standing_set.get(round=finalround).strength  
        gm.team_1.final_rank=gm.team_1.tournament_team_set.get(tournament__lv_id=tournament_id).final_rank        
        gm.team_2.chris_rank=gm.team_2.standing_set.get(round=gm.round).chris_rank        
        gm.team_2.mark_rank=gm.team_2.standing_set.get(round=gm.round).mark_rank        
        gm.team_2.cur_strength=gm.team_2.standing_set.get(round=gm.round).strength        
        gm.team_2.final_strength=gm.team_2.standing_set.get(round=finalround).strength        
        gm.team_2.final_rank=gm.team_2.tournament_team_set.get(tournament__lv_id=tournament_id).final_rank     
    
    stat.percent_overall = '{:3.1f}'.format(100*stat.nr_corwin_overall/stat.nr_games)
    stat.percent_predict = '{:3.1f}'.format(100*stat.nr_corwin_predict/stat.nr_games_predict)
    return render_to_response('powerrank.html',{'upsets': upsets,'teams': tteams, 'stat': stat})

def addtournament(request,tournament_id):
    Tournament.objects.add(tournament_id)
    return HttpResponseRedirect('/powerrank/')
