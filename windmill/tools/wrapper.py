## this module contains leaguevine-calls
## operates on tournament_id basis
## todo: all Windmill logic should be kept out of here... 

from django.utils import simplejson
from django.conf import settings
from django.core.cache import cache
import requests
import logging
import sys
import csv
import itertools
import json
from pprint import pformat

# Get an instance of a logger
logger = logging.getLogger('windmill.tools')

access_token = cache.get('access_token')
if access_token == None:
    # Make a request for an access_token
    if settings.OFFLINE:
        access_token='offline'
    else:
        r=requests.get('http://{0}/oauth2/token/?client_id={1}&client_secret={2}&grant_type=client_credentials&scope=universal'.format(settings.HOST, settings.CLIENT_ID, settings.CLIENT_PWD))
        # parse string into Python dictionary
        r_dict = simplejson.loads(r.content)
        access_token = r_dict.get('access_token')
        cache.set('access_token', access_token)
        logger.info('retrieved a new access token: {0}'.format(access_token))
            
my_headers={'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'bearer {0}'.format(access_token)}  
my_config={'verbose': sys.stderr}

def api_post(url,dict):
    # does a POST on url, sending dict
    datastring=json.dumps(dict)
    logger.info(datastring)
    response=requests.post(url=url,headers=my_headers,config=my_config,data=datastring)
    if response.status_code == 400: # what's that?
        logger.error(response.text)
        response.raise_for_status
    elif response.status_code<>201: # if not "created"
        logger.error(response.status_code)
        logger.error(response.text)
        response.raise_for_status()        
    response_dict = simplejson.loads(response.content)
    logger.info(pformat(response_dict))
    return response_dict    

def api_put(url,dict):
    # does a PUT on url, sending dict
    datastring=json.dumps(dict)
    logger.info('gonna PUT: {0}'.format(pformat(datastring)))
    response=requests.put(url=url,headers=my_headers,config=my_config,data=datastring)
    if response.status_code == 400: # what's that?
        logger.error(response.text)
        response.raise_for_status
    elif response.status_code<>202: # if the update is not "accepted"
        logger.error(response.status_code)
        logger.error(response.text)
        response.raise_for_status()        
    response_dict = simplejson.loads(response.content)
    logger.info(pformat(response_dict))
    return response_dict    

 
def api_tournamentbyid(tournament_id):
    url='http://api.{0}/v1/tournaments/{1}/'.format(settings.HOST,tournament_id)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    return response_dict

def api_nrswissrounds(tournament_id):
# returns the number of existing swissdraw rounds
    url='http://api.{0}/v1/swiss_rounds/?tournament_id={1}&fields=%5Bid%5D'.format(settings.HOST,tournament_id)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    return response_dict['meta']['total_count']

def api_swissroundinfo(tournament_id):
    url='http://api.{0}/v1/swiss_rounds/?tournament_id={1}'.format(settings.HOST,tournament_id)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    return response_dict

def api_poolinfo(tournament_id):
    url='http://api.{0}/v1/pool_rounds/?tournament_id={1}'.format(settings.HOST,tournament_id)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    return response_dict

def api_gamesbytournament(tournament_id):
    url='http://api.{0}/v1/games/?limit=50&tournament_id={1}'.format(settings.HOST,tournament_id)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    return response_dict

def api_gamebyid(game_id):
    url='http://api.{0}/v1/games/{1}/'.format(settings.HOST,game_id)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    return response_dict

def api_bracketsbytournament(tournament_id):
    url='http://api.{0}/v1/brackets/?limit=50&tournament_id={1}'.format(settings.HOST,tournament_id)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    return response_dict

def api_bracketbyid(bracket_id):
    url='http://api.{0}/v1/brackets/{1}/'.format(settings.HOST,bracket_id)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    return response_dict

def api_url(url):
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    logger.info(response_dict)
    return response_dict
    

def api_result(game_id,score1,score2,final=False):
    # upload scores to leaguevine
    url='http://api.{0}/v1/game_scores/'.format(settings.HOST)
    game_dict = {"game_id": "{0}".format(game_id),
                "team_1_score": "{0}".format(score1),
                "team_2_score": "{0}".format(score2),
                "is_final": "{0}".format(final)}
    return api_post(url,game_dict)

def api_clean(tournament_id):
    # retrieve all teams of a particular tournament
    url='http://api.{0}/v1/tournament_teams/?tournament_ids=%5B{1}%5D'.format(settings.HOST,tournament_id) 
    next=True  
    while next:
        # we do not use the next-url, but the original one because we have removed some teams in the meantime
        response = requests.get(url=url,headers=my_headers,config=my_config)
        response_dict = simplejson.loads(response.content)
        logger.info(response_dict)
        
        for team in response_dict.get('objects'):
            # remove this team from tournament
            remove_url='http://api.{0}/v1/tournament_teams/{1}/{2}/'.format(settings.HOST,tournament_id,team.get('team_id'))
            response = requests.delete(url=remove_url,headers=my_headers,config=my_config)
            if response.status_code == 204:
                logger.info('removed team with id {0}'.format(team.get('team_id')))
            else:
                response.raise_for_status()
            
        # check if there are more teams
        next=response_dict.get('meta').get('next')
    return

def api_weblink(tournament_id):
    url='http://api.{0}/v1/tournaments/{1}/'.format(settings.HOST,tournament_id)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    return response_dict.get('leaguevine_url')
    

def api_newtournament(data_dict):
# expects a data_dictionary with leaguevine tournament specification
    url='http://api.{0}/v1/tournaments/'.format(settings.HOST)
    response_dict=api_post(url,data_dict)

    tournament_id = response_dict.get('id')
    logger.info('added tournament with id: {0}'.format(tournament_id))

    return tournament_id

def api_createteam(season_id,name,info):
# creates a new team in season_id with name and info (if does not exists yet)
# returns id of newly created or existing team with this name

    # first check if team with this name already exists in season_id
    logger.info(name)
    url=u'http://api.{0}/v1/teams/?name={1}&season_id={2}'.format(settings.HOST,name,season_id)
    response=requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    if response_dict.get('meta').get('total_count')==0:
        # create a new team in season_id
        url='http://api.{0}/v1/teams/'.format(settings.HOST)
        team_data_dict = {"name": u"{0}".format(name), 
                  "season_id": season_id,
                  "info": "{0}".format(info)}
        response_dict = api_post(url,team_data_dict)
        team_id = response_dict.get('id')
    else:
        # otherwise, get the id from the first object
        team_id = response_dict.get('objects')[0].get('id')
        logger.warning(u'team with name {0} already exists (l_id: {1})'.format(name,team_id))
    
    return team_id


def api_addteam(tournament_id,team_id,seed):
# adds team to tournament
# returns response_dict

    url='http://api.{0}/v1/tournament_teams/'.format(settings.HOST)
    tournament_team_data_dict = {"tournament_id": tournament_id,
                                 "team_id": "{0}".format(team_id),
                                 "seed": "{0}".format(seed) }
    return api_post(url,tournament_team_data_dict)        


def api_addswissround(tournament_id,starttime,pairing='adjacent'):
    
    # TODO: 
    # update the pairing format
#    url='http://api.{0}/v1/tournaments/{1}'.format(settings.HOST,tournament_id)
#    tournament_dict = {"tournament_id": tournament_id,
#                                 "start_time": "{0}".format(starttime),
#                                 "visibility": "live" }    
#    datastring=json.dumps(swissround_dict)
#    logger.info(datastring)
#    response=requests.post(url=url,headers=my_headers,config=my_config,data=datastring)
    
    # create the round
    url='http://api.{0}/v1/swiss_rounds/'.format(settings.HOST)
    swissround_dict = {"tournament_id": tournament_id,
                                 "start_time": "{0}".format(starttime),
                                 "visibility": "live" }
    return api_post(url,swissround_dict)    

def api_cleanbrackets(tournament_id):
    # retrieve all teams of a particular tournament
    url='http://api.{0}/v1/brackets/?tournament_id={1}&fields=%5Bid%5D'.format(settings.HOST,tournament_id) 
    next=True  
    while next:
        # we do not use the next-url, but the original one because we have removed some teams in the meantime
        response = requests.get(url=url,headers=my_headers,config=my_config)
        response_dict = simplejson.loads(response.content)
        logger.info(pformat(response_dict))
        
        for bracket in response_dict.get('objects'):
            # remove this team from tournament
            remove_url='http://api.{0}/v1/brackets/{1}/'.format(settings.HOST,bracket.get('id'))
            response = requests.delete(url=remove_url,headers=my_headers,config=my_config)
            if response.status_code == 204:
                logger.info('removed bracket with id {0}'.format(bracket.get('id')))
            else:
                response.raise_for_status()
            
        # check if there are more teams
        next=response_dict.get('meta').get('next')
    return
    
def api_addbracket(tournament_id,starttime,number_of_rounds,time_between_rounds=180):
    # create the bracket
    url='http://api.{0}/v1/brackets/'.format(settings.HOST)
    bracket_dict = {"tournament_id": tournament_id,
                       "start_time": "{0}".format(starttime),
                       "number_of_rounds": "{0}".format(number_of_rounds),    
                       "time_between_rounds": "{0}".format(time_between_rounds) }
    return api_post(url,bracket_dict)    


def api_addfull3bracket(tournament_id,starttime1,starttime2,starttime3,time_between_rounds=180):
    # creates a full playoff bracket with 3 rounds
    
    # example of full 3-round bracket:
    # http://www.wcbu2011.org/scores/?view=poolstatus&Pool=1009
    
    # create main winner bracket
    url='http://api.{0}/v1/brackets/'.format(settings.HOST)
    bracket_dict = {"tournament_id": tournament_id,
                   "start_time": "{0}".format(starttime1),
                   "number_of_rounds": "3",    
                   "time_between_rounds": "{0}".format(time_between_rounds),
                   "column_position": "0",
                   "row_position": "0",
                   "name": "playoff" }
    response=api_post(url,bracket_dict)
    winnerbr=api_bracketbyid(response['id'])
#    winnerbr=response
    
    # create loser's final
    bracket_dict = {"tournament_id": tournament_id,
                       "start_time": "{0}".format(starttime3),
                       "number_of_rounds": "1",    
                       "time_between_rounds": "{0}".format(time_between_rounds),
                       "column_position": "2",
                       "row_position": "1",
                       "name": "bronze game" }
    response=api_post(url,bracket_dict)
    bronzegame=api_bracketbyid(response['id'])
#    bronzegame=response
    # auto-move losers of semifinal to bronze-game
    for r in winnerbr['rounds']:
        if r['round_number']==1:
            team_nr=1
            for g in r['games']:
                api_loserconnect(g['id'],bronzegame['rounds'][0]['games'][0]['id'],team_nr)
                team_nr += 1
                
    # create lower half of playoff tree (loser's tree)
    bracket_dict = {"tournament_id": tournament_id,
                       "start_time": "{0}".format(starttime2),
                       "number_of_rounds": "2",    
                       "time_between_rounds": "{0}".format(time_between_rounds),
                       "column_position": "1",
                       "row_position": "2",
                       "name": "playoff losers" }
    response=api_post(url,bracket_dict)
    loserstree=api_bracketbyid(response['id'])
#    loserstree=response
    
    # auto-move losers of quarter-finals to loser-tree
    for r in winnerbr['rounds']:
        if r['round_number']==2:
            team_nr=1
            game_nr=0
            for g in r['games']:
                api_loserconnect(g['id'],loserstree['rounds'][0]['games'][game_nr]['id'],team_nr)
                team_nr += 1
                if team_nr == 3:
                    game_nr += 1
                    team_nr = 1
    
    # create game for place 7-8
    bracket_dict = {"tournament_id": tournament_id,
                       "start_time": "{0}".format(starttime3),
                       "number_of_rounds": "1",    
                       "time_between_rounds": "{0}".format(time_between_rounds),
                       "column_position": "2",
                       "row_position": "3",
                       "name": u"game for 7-8" }
    response=api_post(url,bracket_dict)
    placementgame=api_bracketbyid(response['id'])
#    placementgame=response
    # auto-move losers of semifinal to bronze-game
    for r in loserstree['rounds']:
        if r['round_number']==0:
            team_nr=1
            for g in r['games']:
                api_loserconnect(g['id'],placementgame['rounds'][0]['games'][0]['id'],team_nr)
                team_nr += 1
        
def api_loserconnect(source_game,target_game,team_nr):
    # establishes that the loser of source_game
    # becomes team team_nr of target_game
    # where team_nr is 1 or 2

    # weirdly, leaguevine requires start_time and season_id
    # therefore, we retrieve the game info first
    sgame=api_gamebyid(source_game)
    
    url='http://api.{0}/v1/games/{1}/'.format(settings.HOST,source_game)
    game_dict = {"start_time": "{0}".format(sgame['start_time']),
                    "next_game_for_loser": "{0}".format(target_game),    
                    "next_team_for_loser": "{0}".format(team_nr),
                    "season_id": "{0}".format(sgame['season_id'])}
    return api_put(url,game_dict)

def api_setteamsingame(game_id,team_1_id,team_2_id):
    # weirdly, leaguevine requires start_time and season_id
    # therefore, we retrieve the game info first
    game=api_gamebyid(game_id)
    
    url='http://api.{0}/v1/games/{1}/'.format(settings.HOST,game_id)
    game_dict = {"start_time": "{0}".format(game['start_time']),
                 "team_1_id": "{0}".format(team_1_id),    
                 "team_2_id": "{0}".format(team_2_id),
                 "season_id": "{0}".format(game['season_id'])}
    return api_put(url,game_dict)
        
    
def api_addpool(tournament_id,starttime,name,team_ids=[],time_between_rounds=120,generate_matchups=False):
    # create the pool
    url='http://api.{0}/v1/pools/'.format(settings.HOST)
    pool_dict = {"tournament_id": tournament_id,
                   "start_time": "{0}".format(starttime),
                   "name": "{0}".format(name),    
                   "time_between_rounds": "{0}".format(time_between_rounds),
                   "generate_matchups": generate_matchups,
                   "team_ids": team_ids}
    return api_post(url,pool_dict)    
    
def result_in_swissround(round,team_id):
    for g in round['games']:
        if g['team_1_id']==team_id:
            score = g['team_1_score']
            opp_score = g['team_2_score']
        elif g['team_2_id']==team_id:
            score = g['team_2_score']
            opp_score = g['team_1_score']
        else:
            continue
        if score > opp_score:
            return '{0}-{1} win'.format(score,opp_score)
        elif score < opp_score:
            return '{0}-{1} loss'.format(score,opp_score)
        elif score == opp_score:
            return '{0}-{1} tie'.format(score,opp_score)

def rank_in_swissround(round,team_id):
    for t in round['standings']:
        if t['team_id']==team_id:
            return '{0}'.format(t['ranking']) # TODO make ordinal