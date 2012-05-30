from django.utils import simplejson
import urllib2

# Create a new app and copy the credentials it creates
CLIENT_ID = 'a18d62e40f4d269996b01f7cf462a9'
CLIENT_PWD = '93dbb28011a5224303074b3deebaf6'
HOST = "http://api.playwithlv.com"

# Make a request for an access_token
access_token_url = 'http://{0}/oauth2/token/?client_id={1}&client_secret={2}&grant_type=client_credentials&scope=universal'.format(HOST, CLIENT_ID, CLIENT_PWD)
response_data = urllib2.urlopen(access_token_url)

# parse string into Python dictionary
response_dict = simplejson.loads(response_data.read())
response_data.close()
access_token = response_dict.get('access_token')

# Create a JSON object for the new team you want to create
team_data_dict = {"name": "Test Team", 
                  "season_id": 6980,
                  "info": "Test info."}
team_data = simplejson.dumps(team_data_dict)

# Make a request to create a new team
request = urllib2.Request(url='{0}/v1/teams/'.format(HOST), data=team_data)
request.add_header('Content-Type', 'application/json')
request.add_header('Accept', 'application/json')
request.add_header('Authorization', 'bearer {0}'.format(access_token))

response_data = urllib2.urlopen(request)
response_dict = simplejson.loads(response_data.read())

print response_dict