from __future__ import division
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.conf import settings
from windmill.tools.wrapper import *
from windmill.tools.ffindr import *
from windmill.tools.models import Team, Tournament
import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.tools')


def home(request):
    return render_to_response('index.html',{'Tournaments': Tournament.objects.all})

def division(request, div):
    t=Tournament.objects.get(name=div)
    swiss=api_swissroundinfo(t.l_id)
    return render_to_response('division.html',{'div': Tournament.objects.get(name=div),
                                               'swiss': swiss})

def correctresult(game):
    # make up a 'random' result based on the team's seeding information in the local database
    import __builtin__
    t1=Team.objects.get(l_id=game['team_1_id'])
    t2=Team.objects.get(l_id=game['team_2_id'])
    nrteams=t1.tournament.team_set.filter(seed__isnull=False).count()
    logger.info('nr teams: {0}'.format(nrteams))
    diff=(t1.seed - t2.seed)/nrteams
    logger.info(u'game {0} ({2}) vs {1} ({3}), diff: {4}'.format(game['team_1']['name'],game['team_2']['name'],t1.seed,t2.seed, diff))
    if t1.seed > t2.seed:
        s2=15
        s1=min(int(__builtin__.round(15- 15*diff)),14)
    elif t1.seed < t2.seed:
        s1=15
        s2=min(int(__builtin__.round(15+ 15*diff)),14)
    else:
        logger.error('teams have equal seeds, that should not happen')
        raise
    logger.info('computed score: {0} - {1}'.format(s1,s2))
    api_result(game['id'],s1,s2,True)


def randomresults(request, div):
    t=Tournament.objects.get(name=div)
    if div=='women':
#        for url in ["http://api.playwithlv.com/v1/games/?limit=20&tournament_id=18053",
#                    "http://api.playwithlv.com/v1/games/?limit=20&tournament_id=18053&offset=20"]:
#            games=api_url(url)
#            for g in games['objects']:
#                logger.info('game: {0}: {1} - {2}'.format(g['id'],g['team_1_score'],g['team_2_score']))
#
#        return
        
        games=api_gamesbytournament(t.l_id)
        while True:
            for g in games['objects']:
                logger.info('game: {0}: {1} - {2}'.format(g['id'],g['team_1_score'],g['team_2_score']))
                if g['team_1_score']==0 and g['team_2_score']==0:
                    correctresult(g)
            next=games['meta']['next']
            logger.info(u'next: {0}'.format(next))
            if next is None:
                break
            else:
                games=api_url(next)
    else:
        swiss = api_swissroundinfo(t.l_id)
        nrrounds=swiss['meta']['total_count']
        logger.info('nr of rounds: {0}'.format(nrrounds))
        for round in swiss['objects']:
            if round['round_number']==nrrounds: # last round
                logger.info('nr of games: {0}'.format(len(round['games'])))
                for g in round['games']:
                    correctresult(g)

    return render_to_response('index.html',{'Tournaments': Tournament.objects.all})


def ffimport(request):
    ffindr_import()
    return render_to_response('index.html')

def createteams(request):
    for div in ['open', 'mixed', 'women']:
        season_id=settings.SEASON_ID[div]
        for team in Team.objects.filter(tournament__name=div).filter(seed__isnull=False):
            team_id=api_createteam(season_id,team.name,team.id,team.city,team.country_code)
            logger.info('team.l_id before: {0}'.format(team.l_id))
            team.l_id=team_id
            team.save()
            logger.info('team.l_id after:  {0}'.format(team.l_id))

    return render_to_response('index.html')


def addswissround(request, div):
    t=Tournament.objects.get(name=div)
    
    # figure out how many swissdraw rounds already exist
    nrswissrounds=api_nrswissrounds(t.l_id)
    
    # remember that the array counting starts at 0
    # so the following retrieves the data of the *next* round
    starttime=settings.ROUNDS[div][nrswissrounds]['time']
    pairing=settings.ROUNDS[div][nrswissrounds]['mode']
    logger.info("starttime: {0}".format(starttime))
    
    if nrswissrounds!=5:
        # move all but the top 8 teams to the next swiss-draw round
        team_ids=api_rankedteamids(t.l_id,5)
        team_ids=team_ids[8:] # remove the top 8
    else:
        team_ids=[]
    api_addswissround(t.l_id,starttime,pairing,team_ids);
    # TODO: check that field assignments are OK
    return render_to_response('index.html',{'Tournaments': Tournament.objects.all,'div': div})

def addpools(request,div):
    if div<>'women':
        logger.error('something is wrong here')
        raise
    
    t=Tournament.objects.get(name=div)

    # add a pool with all odd seeds
    oddlist=[]
    evenlist=[]
    for team in Team.objects.filter(tournament__name=div):
        if team.seed is None:
            continue
        elif team.seed % 2 == 1:
            oddlist.append(team.l_id)
        elif team.seed % 2 == 0:
            evenlist.append(team.l_id)

    logger.info('oddlist: {0}'.format(oddlist))
    logger.info(evenlist)

    starttime=settings.ROUNDS[div][0]['time']
    # create two pools
    api_addpool(t.l_id,starttime,"Odd Pool",oddlist,120,True)
    api_addpool(t.l_id,starttime,"Even Pool",evenlist,120,True)
    
    
    return render_to_response('index.html',{'Tournaments': Tournament.objects.all,'div': div})
    

def newtourney(request, div):
    season_id=settings.SEASON_ID[div]
    # set up a new tournament
    data_dict = {"name": "Windmill Windup 2012 {0}".format(div), 
             "season_id": season_id,
            "start_date": "2012-06-14",
            "end_date": "2012-06-16",
            "visibility": "live",
            "timezone": "Europe/Amsterdam"}
    if div=='open' or div=='mixed':
        data_dict["scheduling_format"]="swiss"
        data_dict["swiss_scoring_system"]="victory points"
# that's a leaguevine-bug for now...
#        data_dict["swiss_pairing_type"]="adjacent pairing"
    elif div=='women':
        data_dict["scheduling_format"]="regular"
    
    tournament_id=api_newtournament(data_dict)
    t=Tournament.objects.get(name=div)
    t.l_id=tournament_id
    t.save()
        
    link=api_weblink(tournament_id)
    return render_to_response('index.html',{'Tournaments': Tournament.objects.all,'div': div})

def addteams(request, div):
    season_id=settings.SEASON_ID[div]
    t=Tournament.objects.get(name=div)
    if t.l_id is None:
        return HttpResponseNotFound('<h3>Please create tournament first</h3>')
    tournament_id=t.l_id
    
    for team in Team.objects.filter(tournament__name=div):
        if team.seed>0:
            api_addteam(tournament_id,team.l_id,team.seed)
    
    return render_to_response('index.html',{'Tournaments': Tournament.objects.all,'div': div})

    
def clean(request, div):
    t=Tournament.objects.get(name=div)
    api_clean(t.l_id)
    return render_to_response('index.html',{'Tournaments': Tournament.objects.all,'div': div})

def cleanbrackets(request, div):
    season_id=settings.SEASON_ID[div]
    t=Tournament.objects.get(name=div)
    
    api_cleanbrackets(t.l_id)
    return render_to_response('index.html',{'Tournaments': Tournament.objects.all,'div': div})
    
     
def addbracket(request, div):
    season_id=settings.SEASON_ID[div]
    t=Tournament.objects.get(name=div)
    
    api_addfull3bracket(t.l_id,settings.ROUNDS[div][5]['time'],settings.ROUNDS[div][6]['time'],settings.ROUNDS[div][7]['time'])    
    #api_addbracket(t.l_id,settings.ROUNDS[div][5]['time'],3,time_between_rounds=120)
    
    return render_to_response('index.html',{'Tournaments': Tournament.objects.all,'div': div})

def movetoplayoff(request, div):
    season_id=settings.SEASON_ID[div]
    t=Tournament.objects.get(name=div)
    

    if div=='women':
        # do something
        logger.error('women have to be handled here')
    else:
        swiss = api_swissroundinfo(t.l_id)
        nrrounds=swiss['meta']['total_count']
        logger.info('nr of rounds: {0}'.format(nrrounds))
        for round in swiss['objects']:
            if round['round_number']==nrrounds: # last round                
                brackets=api_bracketsbytournament(t.l_id)
                for br in brackets['objects']:
                    if br['number_of_rounds']==3:  # that's the largest bracket
                        api_setteamsingame(br['rounds'][0]['games'][0]['id'],round['standings'][0]['team_id'],round['standings'][7]['team_id'])
                        api_setteamsingame(br['rounds'][0]['games'][1]['id'],round['standings'][4]['team_id'],round['standings'][3]['team_id'])
                        api_setteamsingame(br['rounds'][0]['games'][2]['id'],round['standings'][2]['team_id'],round['standings'][5]['team_id'])
                        api_setteamsingame(br['rounds'][0]['games'][3]['id'],round['standings'][6]['team_id'],round['standings'][1]['team_id'])
                         
                    
    
    return render_to_response('index.html',{'Tournaments': Tournament.objects.all,'div': div})
    