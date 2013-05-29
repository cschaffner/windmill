import logging, logging.config

import groupme_wrapper as gm
import leaguevine_wrapper as lv
from pprint import pformat
import json


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
        'my_logger': {
            'handlers':['console', 'file'],
            'propagate': True,
            'level':'INFO',
        }
    }
}

# FORMAT = '%(asctime)-15s %(message)s'
# logging.basicConfig(format=FORMAT,level=logging.DEBUG)

# Get an instance of a logger
logging.config.dictConfig(LOGGING)

# create logger with 'spam_application'
logger = logging.getLogger('my_logger')

# tournament ids: 
OPEN = u'19176'
LADIES = u'19177'
MIXED = u'19178'

def create_team_dict():
    team_dict = {}
    
    for tournament_id in [LADIES, MIXED, OPEN]:
        teams = lv.api_tournament_teams(tournament_id)
        for team in teams['objects']:
            team_dict[team['team_id']] = team['team']
            team_dict[team['team_id']][u'tournament_id'] = tournament_id
    
    for team_id, team in team_dict.iteritems():
        group = gm.api_submit_group(team['name'])
        team[u'group_id'] = group['group_id']
        team[u'share_url'] = group['share_url']
        
    logger.info(pformat(team_dict))
    return team_dict

def read_web():
    from ww13_fixture import web_string, team_dict
    import re
    for line in web_string.split('\n'):
        parts = line.split('<li')
        team_name = parts[1][1:].split('</li>')[0].strip()
        country = parts[2][17:].split('</li>')[0].strip()
        status = parts[3][1:].split('</li>')[0].strip()
        
        # find in team_dict
        found = False
        for team_id, team in team_dict.iteritems():
            if team['name'].lower() == team_name.lower():
                team[u'country'] = country
                team[u'status'] = status
                found = True                    
                break
        if not found:
            logger.error(team_name)
#            raise
    
    logger.info(pformat(team_dict))    

def write_web():
    team_dict = json.load(open('team_dict.json'))
    
    for tournament_id in [OPEN, LADIES, MIXED]:
        print '\n\n'
        print u'<li>TEAMS</li><li class="country">COUNTRY</li><li class="groupme">GroupMe</li><li>PAID TO DATE</li>'
        for team_id, team in team_dict.iteritems():
            if team['tournament_id'] == tournament_id:
                string = '<li><a target="_blank" href="{0}">{1}</a></li><li class="country">{2}</li>'.format(team['leaguevine_url'], team['name'], team['country'])
                string += '<li class="groupme"><a target="_blank" href="{0}">join</a></li><li>{1}</li>'.format(team['share_url'], team['status'])
                print string

def write_excel():
    team_dict = json.load(open('team_dict.json'))    
    for tournament_id in [OPEN, LADIES, MIXED]:
        print '\n\n'
        for team_id, team in team_dict.iteritems():
            if team['tournament_id'] == tournament_id:
                string = '{0}\t{1}'.format(team['name'], team['share_url'])
                print string

def write_numbers():
    team_dict = json.load(open('team_dict.json'))    
    for tournament_id in [OPEN, LADIES, MIXED]:
        print '\n\n'
        for team_id, team in team_dict.iteritems():
            if team['tournament_id'] == tournament_id:
                string = '{1}\t{2}\t{3}\t{0}'.format(team['name'], team['nr_members_groupme'], team['nr_members_lv'], team['nr_claimed_lv'])
                print string

            
def change_avatar():
    team_dict = json.load(open('team_dict.json'))   
    for team_id, team in team_dict.iteritems():
        response = gm.api_change_group(team['group_id'], None, None, u'http://i.groupme.com/9e1882509c600130f2485a84f3f294ce', True)
        logger.info(response)

def add_bots():
    team_dict = json.load(open('team_dict.json'))   
    for team_id, team in team_dict.iteritems():
        response = gm.api_submit_bot(u'Herbie',
                                     team['group_id'],
                                     u'http://i.groupme.com/12b1f9e09d8a013075a04681181770fd',
                                     u'http://windmill.herokuapp.com/groupme/bot_callback/')
        logger.info(response)
        team[u'bot_id'] = response['bot_id']
    logger.info(pformat(team_dict))

def kill_all_bots():
    team_dict = json.load(open('team_dict.json'))
    for team_id, team in team_dict.iteritems():
        if u'bot_id' in team:
            logger.info(gm.api_kill_bot(team['bot_id']))
            del team['bot_id']
    logger.info(pformat(team_dict))
        

def tell_ladies(text):
    team_dict = json.load(open('team_dict.json'))
    for team_id, team in team_dict.iteritems():
        if team['tournament_id'] == LADIES:
            gm.api_bot_message(team['bot_id'], text)

def tell_mixed(text):
    team_dict = json.load(open('team_dict.json'))
    for team_id, team in team_dict.iteritems():
        if team['tournament_id'] == MIXED:
            gm.api_bot_message(team['bot_id'], text)

def tell_open(text):
    team_dict = json.load(open('team_dict.json'))
    for team_id, team in team_dict.iteritems():
        if team['tournament_id'] == OPEN:
            gm.api_bot_message(team['bot_id'], text)

def tell_all(text):
    team_dict = json.load(open('team_dict.json'))    
    for team_id, team in team_dict.iteritems():
        gm.api_bot_message(team['bot_id'], text)
    
def lv_message():
    team_dict = json.load(open('team_dict.json')) 
    for team_id, team in team_dict.iteritems():
        text = u"I'm getting lazy after all these years and I need you, my beloved players, to upload your own scores via Leaguevine. " 
        text += u"As preparation, please go to your team page {0}roster/ ".format(team['leaguevine_url'])
        text += u"and fill in your team roster."   
        gm.api_bot_message(team['bot_id'], text)

def update_nr_members():
    from ww13_fixture import team_dict_with_bots
    team_dict = team_dict_with_bots
#    team_dict = json.load(open('team_dict.json'))
    for team_id, team in team_dict.iteritems():
        group = gm.api_get_group(team['group_id'])['response']
        nr_players, nr_claimed = lv.api_number_players_in_team(team_id)
        team['nr_members_groupme'] = len(group['members'])
        team['nr_members_lv'] = nr_players
        team['nr_claimed_lv'] = nr_claimed
    json.dump(team_dict, open('team_dict.json','w'), indent=3)

        
if __name__ == "__main__":
    lv_message()
    
#     update_nr_members()
#     write_numbers()

#    tell_all(u"I'm Herbie and I will keep you posted on the latest and greatest at the Windmill Windup 2013! If you have any questions, send me a message at herbie@windmillwindup.com")
