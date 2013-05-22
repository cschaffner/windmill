import logging, logging.config
import requests # To install this library: pip install requests
import json 
import sys
import StringIO
import xlrd
import string
import re
import csv
import itertools

from pprint import pformat

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'file': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'file',
            'filename': 'log.log',
            'maxBytes': '1024',
            'backupCount': '10',  
        }
    },
    'loggers': {
        'ffindr': {
            'handlers':['console','file'],
            'propagate': True,
            'level':'INFO',
        }
    }
}

#FORMAT = '%(asctime)-15s %(message)s'
#logging.basicConfig(format=FORMAT,level=logging.DEBUG)

# Get an instance of a logger
logging.config.dictConfig(LOGGING)

# create logger with 'spam_application'
logger = logging.getLogger('ffindr')

PREV_SEASON_ID={u'open': 20068,
                u'women': 20069,
                u'mixed': 20067}


SEASON_ID={u'open': 20183,
           u'women': 20184,
           u'mixed': 20277}

TOURNAMENT_ID = {u'open': 19176,
                 u'women': 19177,
                 u'mixed': 19178}

# Create a new app and copy the credentials it creates
CLIENT_ID = '0920660af4b0c2ba01c9df96385d9b'
CLIENT_PWD = '1bd5ebdde1552c08c626fc2ce35238'
#BASE_API_URL = "http://api.playwithlv.com"
#TOKEN_URL = 'http://www.playwithlv.com'    
BASE_API_URL = "https://api.leaguevine.com"
TOKEN_URL = 'https://www.leaguevine.com'    
ONLINE = True

access_token = os.environ['LEAGUEVINE_TOKEN']
if access_token == None:
    # Make a request for an access_token
    url='{0}/oauth2/token/?client_id={1}&client_secret={2}&grant_type=client_credentials&scope=universal'.format(TOKEN_URL , CLIENT_ID, CLIENT_PWD)
    if ONLINE:
        r=requests.get(url)
        # parse string into Python dictionary
        r_dict = json.loads(r.content)
        access_token = r_dict.get('access_token')
        logger.info(access_token)
    
# save headers for this session
my_headers={'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'bearer {0}'.format(access_token)}  
my_config={'verbose': sys.stderr}


def shortName(longName):
    # split off number if there is any
    if longName[-1].isdigit():
        return teamdict[longName.rstrip('0123456789 ')]+longName[-1]
    else:
        return teamdict[longName]

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
    response_dict = json.loads(response.content)
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
    elif response.status_code==403: # FORBIDDEN
        logger.error('not enough rights to update {0} {1}, id: {2}'.format(dict['first_name'],dict['last_name'],url[-6:-1]))
        logger.error(pformat(dict))
    elif response.status_code<>202: # if the update is not "accepted"
        logger.error(response.status_code)
        logger.error(response.text)
        response.raise_for_status()        
    response_dict = json.loads(response.content)
    logger.info(pformat(response_dict))
    return response_dict    

def api_update(url,updatedict={}):
    # first retrieves the data of an object
    # then merges the fields with updatedict
    # and PUTs it again
    # works e.g. for tournaments and games

    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = json.loads(response.content)
    
    new_dict={}
    for key,val in response_dict.iteritems():
        if ((val is not None) and (not isinstance(val, dict)) and (key != 'leaguevine_url') and 
            (key != 'resource_uri') and (key!='time_last_updated') and (key!='time_created') and
            (key != 'objects')):
            new_dict[key]=val
            # fix a leaguevine bug here:
            if key=="start_time" and val[-6:]=="+01:20":
                new_dict[key]=val[:-6]+"+02:00"
                
    logger.info('before updating: {0}'.format(pformat(new_dict)))
    new_dict.update(updatedict)
    logger.info('after updating: {0}'.format(pformat(new_dict)))
    
    return api_put(url,new_dict)


def submitTeam(teamname,country=None,division=None):        
    url='{0}/v1/teams/?name={1}&season_id={2}'.format(BASE_API_URL,teamname,SEASON_ID[division]) 
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = json.loads(response.content)
    logger.info(response_dict)
    if response_dict['meta']['total_count']==1:
        return response_dict['objects'][0]
    else:
        # create team
        data={'name': teamname,
              'season_id': SEASON_ID[division]}
        if not country is None:
            data['country']=country
        # check if team exists in previous season in order to "link" teams
        url='{0}/v1/teams/?name={1}&season_id={2}'.format(BASE_API_URL,teamname,PREV_SEASON_ID[division]) 
        response = requests.get(url=url,headers=my_headers,config=my_config)
        response_dict = json.loads(response.content)
        if response_dict['meta']['total_count']==1:
            data['related_team_ids']=[response_dict['objects'][0]['id']]
            
        url='{0}/v1/teams/'.format(BASE_API_URL)
        response_dict=api_post(url,data)
        return response_dict

def submitPlayer(first_name,last_name,test=False):        
    # prefer claimed players, because those have been created by actual people
    url='{0}/v1/players/?name={1}%20{2}&order_by=%5Bis_claimed%5D'.format(BASE_API_URL,first_name,last_name) 
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = json.loads(response.content)
#    logger.info(response_dict)
    if test:
        if response_dict['meta']['total_count']==1:
            return response_dict['objects'][0]
        else:
            logger.error('multiple possible players found!')
            return False
    if response_dict['meta']['total_count']==1:
        player=response_dict['objects'][0]
        if player['first_name']==first_name and player['last_name']==last_name and (player['is_claimed'] or (not player['is_claimed'] and not player['indexable'])):
            logger.info('everything OK')
            return player
        else:
            logger.warning('player {0} {1} is being updated!'.format(first_name,last_name))
            url='{0}/v1/players/{1}/'.format(BASE_API_URL,player['id'])
            data={'first_name': first_name,
                  'last_name': last_name}
            if not player['is_claimed']:  # if player is not claimed, set indexable flag to False
                data['indexable']=False;  # otherwise, leave it up to the claimed player to decide
            response_dict=api_update(url,data)
            return response_dict
    elif response_dict['meta']['total_count']>1:
        print('{0} profiles found'.format(response_dict['meta']['total_count']))
        prof_ind=[]
        for idx,player in enumerate(response_dict['objects']):
            prof_ind.append(player['id'])
            print('Profile #{0}'.format(idx))
            print([player['id'],player['first_name'],player['last_name'],player['is_claimed']])
            if player['first_name']==first_name and player['last_name']==last_name:
                prof=idx
            url='{0}/v1/team_players/?player_ids=%5B{1}%5D'.format(BASE_API_URL,player['id']) 
            response = requests.get(url=url,headers=my_headers,config=my_config)
            response_dict = json.loads(response.content)
            print('Teams ({0}):'.format(response_dict['meta']['total_count']))
            if response_dict['meta']['total_count']>0:
                for team_player in response_dict['objects']:
                    print(team_player['team']['name'])
            else:
                logger.warning('player with id: {0} is being removed (because she is not a teamplayer...)!'.format(player['id']))
                # remove this player!
                url='{0}/v1/players/{1}/'.format(BASE_API_URL,player['id'])
                #response = requests.delete(url=url,headers=my_headers,config=my_config)

#        prof=input('which profile should be used? ({0})'.format(prof))
        merg1=raw_input('merge profile nr 1:')
        if not merg1=='':
            merg2=raw_input('merge profile nr 2:')
            merg1_id=prof_ind[int(merg1)]
            merg2_id=prof_ind[int(merg2)]
            logger.info('should we merge {0} with {1}?'.format(merg1_id,merg2_id))
            url='{0}/v1/players/merge/{1}/{2}/'.format(BASE_API_URL,merg1_id,merg2_id)
            response = requests.post(url=url,headers=my_headers,config=my_config)
            if response.status_code==403: # not enough rights
                # go through teams of second player
                url='{0}/v1/team_players/?player_ids=%5B{1}%5D'.format(BASE_API_URL,merg2_id) 
                response = requests.get(url=url,headers=my_headers,config=my_config)
                response_dict = json.loads(response.content)
                if response_dict['meta']['total_count']>0:
                    for team_player in response_dict['objects']:
                        logger.info('adding team {0} to 1st player'.format(team_player['team']['name']))
                        # add team to first player
                        submitTeamPlayer(merg1_id,team_player['team']['id'])
                else:
                    logger.warning('2nd player does not have any teams to add to the first')
                # second player can now be removed:
                url='{0}/v1/players/{1}/'.format(BASE_API_URL,merg2_id)
                response = requests.delete(url=url,headers=my_headers,config=my_config)
            return submitPlayer(first_name,last_name)
        
    
    url='{0}/v1/players/'.format(BASE_API_URL)
    data={'first_name': first_name,
          'last_name': last_name,
          'indexable': False}
#    response_dict=api_post(url,data)
    return response_dict

def submitTeamPlayer(player_id,team_id):        
    url='{0}/v1/team_players/{1}/{2}/'.format(BASE_API_URL,team_id,player_id) 
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = json.loads(response.content)
    logger.info(response_dict)
    if u'error_message' in response_dict:
        url='{0}/v1/team_players/'.format(BASE_API_URL)
        data={'team_id': team_id,
              'player_id': player_id}
        response_dict=api_post(url,data)
        return response_dict
    else:
        return response_dict


def submittournament(tournament_name,date):        
    url='{0}/v1/tournaments/?name={1}&season_id={2}'.format(BASE_API_URL,tournament_name,season_id) 
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = json.loads(response.content)
    logger.info(response_dict)
    if response_dict['meta']['total_count']==1:
        tournament_dict=response_dict['objects'][0] 
    else:
        url='{0}/v1/tournaments/'.format(BASE_API_URL)
        data={'name': tournament_name,
              'season_id': season_id,
              'start_date': date,
              'end_date': date,
              'timezone': 'Europe/Amsterdam',
              'uses_seeds': False}
        tournament_dict=api_post(url,data)
    
    # make sure that all teams of this season are tournament teams of this tournament
    url='{0}/v1/teams/?season_id={1}&limit=200'.format(BASE_API_URL,season_id) 
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = json.loads(response.content)
    logger.info(response_dict)
    for team in response_dict['objects']:
        url='{0}/v1/tournament_teams/'.format(BASE_API_URL)
        data={'tournament_id': tournament_dict['id'],
              'team_id': team['id']}
        response_dict=api_post(url,data)
        if response_dict.has_key(u'errors'):
            #  probably these teams have already been added to this tournament
            break
    
    return tournament_dict
        

def readTeamNames():
#    wb = xlrd.open_workbook('Open12/open2012.xls')
#    wb = xlrd.open_workbook('Mixed12/mixed2012.xls')
    wb = xlrd.open_workbook(workbook)
    logger.info(wb.sheet_names())
    sh = wb.sheet_by_index(0)
    on = False
    dict = {}
    lvdict = {}
    for rownum in range(sh.nrows):
        if on:
            teamname=sh.row_values(rownum)[1]
            shortname=sh.row_values(rownum)[0]
            lv_info=submitteam(teamname,shortname)
            lv_info['short_name']=shortname
            lvdict[teamname]=lv_info
            dict[teamname.rstrip('0123456789 ')]=shortname.rstrip('0123456789 ')            
        if "Teamnaam" in sh.row_values(rownum)[0]:
            on=True
    logger.info(pformat(lvdict))
    return lvdict

def rosters():
#    lvdict=TeamNamesMixed12()
#    lvdict=TeamNamesOpen12()
    lvdict=TeamNamesIndoor12()
#    lvdict=readTeamNames()
    wb = xlrd.open_workbook(workbook)
    logger.info(wb.sheet_names())
    sh = wb.sheet_by_name(u'teamlist')
    playersstartat=sh.col_values(0).index('spelers')+1
    teamnameat=sh.col_values(0).index('team naam')
    
    for colnum in range(20,sh.ncols): #sh.ncols
        teamname=sh.col_values(colnum)[teamnameat]
        team_id=lvdict[teamname]['id']
        rownum=playersstartat
        playername=sh.col_values(colnum)[rownum].strip()
        while playername!='':
            if playername.count('Reint')>0:
                logger.info('wait')
            playername=playername.replace(u'\xa0', u' ')

      
            pat_first = r"""(?P<first>\b[\w\-]+\b)"""
            pat_firsts = r"""(?P<first>(\b[\w\-]+\b\s*)+)"""
            pat_tussen = r"""(?P<tussen>van\sder|van\sden|van\sde|van|den|ten|ter|te|de|v\.d\.)"""
            pat_last = r"""(?P<last>\b[\w+\-]+\b)"""
            pat_lasts = r"""(?P<last>([\w\-]+\s*)+)"""
            
            pat1 = re.compile(r"""
            ^\s*                    # Skip leading whitespace
            """ + pat_first + r"""  # first name
            \s*                     # Whitespace
            """ + pat_tussen + r"""? # possible Dutch middle words
            \s*                     # whitespace
            """ + pat_last + r"""   # last name
            \s*$                    # Trailing whitespace to end-of-line            
            """, re.VERBOSE|re.UNICODE)            
            
            pat2 = re.compile(r"""
            ^\s*                    # Skip leading whitespace
            """ + pat_first + r"""  # first name
            \s*                     # Whitespace
            """ + pat_last + r"""   # last name
            ,\s*                    # comma, whitespace
            """ + pat_tussen + r"""+ # mandatory Dutch middle words
            \s*$                    # whitespace and end-of line
            """, re.VERBOSE|re.UNICODE)

            pat3 = re.compile(r"""        
            ^\s*                    # Skip leading whitespace
            """ + pat_lasts + r"""   # last name
            \,\s*                   # comma, followed by whitespace
            """ + pat_firsts + r"""  # (multiple) first names
            \s*                     # Trailing whitespace 
            """ + pat_tussen + r"""+ # mandatory Dutch middle words
            \s*$                    # whitespace to end-of-line
            """, re.VERBOSE|re.UNICODE)

            pat4 = re.compile(r"""        
            ^\s*                    # Skip leading whitespace
            """ + pat_last + r"""   # last name
            \,\s*                   # comma, followed by whitespace
            """ + pat_tussen + r"""+ # mandatory Dutch middle words
            \,\s*                   # comma, followed by whitespace
            """ + pat_first + r"""  # first name
            \s*$                    # whitespace
             """, re.VERBOSE|re.UNICODE)

            pat5 = re.compile(r"""        
            ^\s*                    # Skip leading whitespace
            """ + pat_lasts + r"""   # last name
            \,\s*                   # comma, followed by whitespace
            """ + pat_firsts + r"""  # (multiple) first names
            \s*                     # Trailing whitespace 
            """ + pat_tussen + r"""? # possible Dutch middle words
            \s*$                    # whitespace to end-of-line
            """, re.VERBOSE|re.UNICODE)

            m=pat1.search(playername.lower())
            if not m:
                logger.info('{0}'.format(playername))
                m=pat2.search(playername.lower())
                if not m:
                    m=pat3.search(playername.lower())
                    if not m:
                        m=pat4.search(playername.lower())
                        if not m:
                            m=pat5.search(playername.lower())
                            if not m:
                                logger.error('no pattern matched')
                                # check online if we figured it out already...
                                player=submitPlayer(playername,'',True)
                                if player==False:
                                    logger.error('failed')
                                else:
                                    logger.info('{0}#{1}'.format(player['first_name'],player['last_name']))
            
            if m:
                first_name=m.group('first').title()
                if m.group('tussen') != None:
                    last_name='{0} {1}'.format(m.group('tussen'),m.group('last').title())
                else:
                    last_name=m.group('last').title()
                logger.info('{0}#{1}'.format(first_name,last_name))
                
            player=submitPlayer(first_name,last_name)
#            team_player=submitTeamPlayer(player['id'],team_id)
           
            
            rownum += 1
            playername=sh.col_values(colnum)[rownum].strip()            
 
def create_compday():
    lvdict=TeamNamesIndoor12()
    
    day=3
    date=dates[day-1]
    tournament=submittournament('Speeldag {0}'.format(day),date)
    
    for divisie in range(1,9):
        wb = xlrd.open_workbook('Indoor1213/schema_dag{0}.xls'.format(day))
        rowstart=1
        sh = wb.sheet_by_index(divisie-1)
        on = False
        pool_teams = []
        pool_team_ids = []
        rownum=rowstart
        while sh.row_values(rownum)[8] != "":
            pool_teams.append(sh.row_values(rownum)[8])
            pool_team_ids.append(lvdict[sh.row_values(rownum)[8]]['id'])
            rownum += 1
        logger.info(pool_team_ids)
    
        # create or get pool
        time=xlrd.xldate_as_tuple(sh.row_values(rowstart)[1], 0) 
        start_time='{0}T{1:02}:{2:02}:00+01:00'.format(date,time[3],time[4])
        pool=submitPool('{0}e divisie'.format(divisie),start_time,tournament['id'],pool_team_ids)
        pool_round=submitPoolRound(pool['id'],start_time)
        
        # add games and scores
        reswb = xlrd.open_workbook(workbook)
        ressh = reswb.sheet_by_index(day-1)
        # for a full round robin
        nrgames=(len(pool_team_ids)*(len(pool_team_ids)-1))/2
        
        for rownum in range(rowstart,rowstart+nrgames+1):
            timevalue=sh.row_values(rownum)[1]
            if timevalue=="":
                continue
            time=xlrd.xldate_as_tuple(timevalue, 0) 
            start_time='{0}T{1:02}:{2:02}:00+01:00'.format(date,time[3],time[4])
            team_1_name=sh.row_values(rownum)[3]
            team_2_name=sh.row_values(rownum)[5]
            team_1_id=lvdict[team_1_name]['id']
            team_2_id=lvdict[team_2_name]['id']
            pool_round_id = pool_round['id']
            game = submitGame(start_time,team_1_id,team_2_id,pool_round_id)
        
            if WITHSCORE:
                # figure out score
                # find row where results are listed
                for startsat in range(ressh.nrows):
                    if ressh.row_values(startsat)[0]=='{0}e divisie'.format(divisie):
                        startsat += 1
                        break
            
                team_1_ind=ressh.row_values(startsat).index(lvdict[team_1_name]['short_name'])
                team_2_ind=ressh.row_values(startsat).index(lvdict[team_2_name]['short_name'])
                if team_1_ind==0:
                    logger.error('the result of team with short name {0} was not found'.format(lvdict[team_1_name]['short_name']))
                    raise
                elif team_2_ind==0:
                    logger.error('the result of team with short name {0} was not found'.format(lvdict[team_2_name]['short_name']))
                    raise            
                elif team_1_ind < team_2_ind:
                    # get score
                    score = ressh.row_values(startsat+team_1_ind)[team_2_ind].strip(' \t')
                    team_1_score,sep,team_2_score=score.partition('-')
                elif team_1_ind > team_2_ind:
                    # get score
                    score = ressh.row_values(startsat+team_2_ind)[team_1_ind].strip(' \t')
                    team_2_score,sep,team_1_score=score.partition('-')
        
                if game['team_1_score']!=team_1_score or game['team_2_score']!=team_2_score or game['is_final']==False:
                    url='{0}/v1/game_scores/'.format(BASE_API_URL) 
                    data={'game_id': game['id'],
                          'team_1_score': team_1_score,
                          'team_2_score': team_2_score,
                          'is_final': True}
                    response_dict=api_post(url,data)
        
        
def create_last_compday():
    lvdict=TeamNamesIndoor11()
    
    day=4
    date=dates[day-1]
    tournament=submittournament('Speeldag {0}'.format(day),date)
    
    
    for divisie in range(1,8): # 7 divisions
        wb = xlrd.open_workbook('Indoor1112/schema_dag{0}.xls'.format(day))
        sh = wb.sheet_by_index(1)
        sh_time = wb.sheet_by_index(0)
        pool_teams = []
        pool_team_ids = []
        rownum=1
        for game in sh.col_values(divisie-1)[1:]:
            team1,sep,team2=game.partition(' - ')
            if not team1 in pool_teams:
                pool_teams.append(team1)
                pool_team_ids.append(lvdict[team1]['id'])
            if not team2 in pool_teams:
                pool_teams.append(team2)
                pool_team_ids.append(lvdict[team2]['id'])
        logger.info(pool_team_ids)
    
        # create or get pool
        start_time='{0}T10:05:00+01:00'.format(date)
        pool=submitPool('{0}e divisie'.format(divisie),start_time,tournament['id'],pool_team_ids)
        pool_round=submitPoolRound(pool['id'],start_time)
        
        # add games and scores
        reswb = xlrd.open_workbook(workbook)
        ressh = reswb.sheet_by_index(day-1)
        # for a full round robin
        nrgames=(len(pool_team_ids)*(len(pool_team_ids)-1))/2
        
        for gamestring in sh.col_values(divisie-1)[1:]:
            
            # figure out starting time
            rownum=sh_time.col_values(2).index(gamestring)
            timevalue=sh_time.row_values(rownum)[0]
            if timevalue=="":
                raise
            time=xlrd.xldate_as_tuple(timevalue, 0) 
            start_time='{0}T{1:02}:{2:02}:00+01:00'.format(date,time[3],time[4])
            team_1_name,sep,team_2_name=game.partition(' - ')
            team_1_id=lvdict[team_1_name]['id']
            team_2_id=lvdict[team_2_name]['id']
            pool_round_id = pool_round['id']
            game = submitGame(start_time,team_1_id,team_2_id,pool_round_id)
            
            # figure out score
            # find row where results are listed
            for startsat in range(ressh.nrows):
                if ressh.row_values(startsat)[0]=='{0}e divisie'.format(divisie):
                    startsat += 1
                    break
        
            team_1_ind=ressh.row_values(startsat).index(lvdict[team_1_name]['short_name'])
            team_2_ind=ressh.row_values(startsat).index(lvdict[team_2_name]['short_name'])
            if team_1_ind==0:
                logger.error('the result of team with short name {0} was not found'.format(lvdict[team_1_name]['short_name']))
                raise
            elif team_2_ind==0:
                logger.error('the result of team with short name {0} was not found'.format(lvdict[team_2_name]['short_name']))
                raise            
            elif team_1_ind < team_2_ind:
                # get score
                score = ressh.row_values(startsat+team_1_ind)[team_2_ind].strip(' \t')
                team_1_score,sep,team_2_score=score.partition('-')
            elif team_1_ind > team_2_ind:
                # get score
                score = ressh.row_values(startsat+team_2_ind)[team_1_ind].strip(' \t')
                team_2_score,sep,team_1_score=score.partition('-')
    
            url='{0}/v1/game_scores/'.format(BASE_API_URL) 
            data={'game_id': game['id'],
                  'team_1_score': team_1_score,
                  'team_2_score': team_2_score,
                  'is_final': True}
            response_dict=api_post(url,data)
        

def read_country_codes():
    """ returns a dictionary with country names as keys and ISO alpha-2 code as values """ 
    
    with open('/Users/chris/Sites/windmill/windmill/regdata/country_codes.csv', 'rU') as csvfile:
        csvfile.seek(0)
        countries = csv.reader(csvfile, delimiter=';', quotechar='|')
        country_code={}
        for country in itertools.islice(countries,1,300):
            country_code[country[0].strip()]=country[1].strip()
    
    return country_code

def upload_teams():
    country_code=read_country_codes()
    division=u'mixed'
    teams=csv.reader(open('/Users/chris/Sites/windmill/windmill/regdata/{0}_2013.csv'.format(division)))

    for team in itertools.islice(teams,1,200):
        try:
            cc=country_code[team[14]]
        except KeyError:
            cc=None
        response=submitTeam(team[0],cc,division)
        logger.debug(pformat(response))

def upload_players():
    division = u'mixed'
    teams =c sv.reader(open('/Users/chris/Sites/windmill/windmill/regdata/{0}_2013.csv'.format(division)))

    for team in itertools.islice(teams, 1, 200):
        response = submitPlayer(team[0], cc, division)
        logger.debug(pformat(response))
    

def tournament_teams():    
    tournament_id=18091
    # retrieve all teams of a particular tournament
    url='{0}/v1/tournament_teams/?tournament_ids=%5B{1}%5D'.format(BASE_API_URL,tournament_id) 
    next=url  
    while next:
        # we do not use the next-url, but the original one because we have removed some teams in the meantime
        response = requests.get(url=next,headers=my_headers,config=my_config)
        response_dict = json.loads(response.content)
        logger.info(response_dict)
        
        for team in response_dict.get('objects'):
            logger.info('found team with id {0}'.format(team.get('team_id')))
            
        # check if there are more teams
        next=response_dict.get('meta').get('next')


if __name__ == "__main__":
    upload_players()
    #create_compday()