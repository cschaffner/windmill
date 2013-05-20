import logging, logging.config
import groupme_wrapper as gm
import leaguevine_wrapper as lv
from pprint import pformat
from random import randint

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
logger = logging.getLogger('my_logger')

# tournament ids: 
OPEN = u'19176'
LADIES = u'19177'
MIXED = u'19178'

def make_seedings():
    from ww13_fixture import team_dict
    seeding = {}
    for tournament_id in [OPEN, LADIES, MIXED]:
        seed = 1
        for team_id, team in team_dict.iteritems():
            if team['tournament_id'] == tournament_id:
                seeding[team_id] = seed
                seed += 1
    logger.info(pformat(seeding))
           
def show_seeding(tournament_id):
    from ww13_fixture import seeding, team_dict
    for team_id, team in team_dict.iteritems():
        if team['tournament_id'] == tournament_id:
            print 'seed: {0} - {1}'.format(seeding[team_id],team['name']) 
    

def fill_results(tournament_id):
    from ww13_fixture import seeding
    
    nr_swissrounds = lv.api_nrswissrounds(tournament_id)
    last_round = lv.api_swissroundinfo(tournament_id, nr_swissrounds)
    for game in last_round['objects'][0]['games']:
        if game['team_1_score'] == 0 and game['team_2_score'] == 0:
            # make up "random" score according to seeding
            team_1_id = game['team_1_id']
            team_2_id = game['team_2_id']
            seed_1 = seeding[team_1_id]
            seed_2 = seeding[team_2_id]
            if seed_1 < seed_2:
                team_1_score = randint(13,15)
                team_2_score = max(0, team_1_score - (seed_2 - seed_1))
                team_2_score += randint(0,2)
            else:
                team_2_score = randint(13,15)
                team_1_score = max(0, team_2_score - (seed_1 - seed_2))
                team_1_score += randint(0,2)
            lv.api_result(game['id'], team_1_score, team_2_score, True)
        
if __name__=="__main__":
#    show_seeding(MIXED)
    fill_results(MIXED)