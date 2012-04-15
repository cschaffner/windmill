# now using requests
import requests

# Get an instance of a logger
logger = logging.getLogger('leaguevine.addons')

# Create a new app and copy the credentials it creates
CLIENT_ID = 'a18d62e40f4d269996b01f7cf462a9'
CLIENT_PWD = '93dbb28011a5224303074b3deebaf6'
HOST = "playwithlv.com"

# Make a request for an access_token
r=requests.get('http://{0}/oauth2/token/?client_id={1}&client_secret={2}&grant_type=client_credentials&scope=universal'.format(HOST, CLIENT_ID, CLIENT_PWD))
# parse string into Python dictionary
r_dict = simplejson.loads(r.content)
access_token = r_dict.get('access_token')
logger.info(access_token)

# save headers for this session
my_headers={'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'bearer {0}'.format(access_token)}  
my_config={'verbose': sys.stderr}

# retrieve all teams of a particular tournament
url='http://api.{0}/v1/tournament_teams/?tournament_ids=%5B{1}%5D'.format(HOST,tournament_id) 
next=True  
while next:
    # we do not use the next-url, but the original one because we have removed some teams in the meantime
    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    logger.info(response_dict)
    
    for team in response_dict.get('objects'):
        # remove this team from tournament
        remove_url='http://api.{0}/v1/tournament_teams/{1}/{2}/'.format(HOST,tournament_id,team.get('team_id'))
        response = requests.delete(url=remove_url,headers=my_headers,config=my_config)
        if response.status_code == 204:
            logger.info('removed team with id {0}'.format(team.get('team_id')))
        else:
            response.raise_for_status()
        
    # check if there are more teams
    next=response_dict.get('meta').get('next')

 