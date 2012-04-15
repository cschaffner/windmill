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

# Get an instance of a logger
logger = logging.getLogger('leaguevine.addons')

access_token = cache.get('access_token')
if access_token == None:
    # Make a request for an access_token
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
    logger.info(response_dict)
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

def api_addbracket(tournament_id,starttime,number_of_rounds,time_between_rounds=120):
    # create the bracket
    url='http://api.{0}/v1/brackets/'.format(settings.HOST)
    bracket_dict = {"tournament_id": tournament_id,
                       "start_time": "{0}".format(starttime),
                       "number_of_rounds": "{0}".format(number_of_rounds),    
                       "time_between_rounds": "{0}".format(time_between_rounds) }
    return api_post(url,bracket_dict)    
    
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
    
    