import urllib2
import ast

# Windmill tournament info on leaguevine:
#{
#    "end_date": "2012-06-17",
#    "id": 18029,
#    "info": "",
#    "leaguevine_url": "http://playwithlv.com/tournaments/18029/windmill-windup/",
#    "name": "Windmill Windup",
#    "number_of_sets": null,
#    "resource_uri": "http://api.playwithlv.com/v1/tournaments/18029/",
#    "scheduling_format": "swiss",
#    "season": {
#        "end_date": "2011-12-31",
#        "id": 6980,
#        "league": {
#            "id": 6979,
#            "leaguevine_url": "http://playwithlv.com/leagues/6979/club-open/",
#            "name": "Club Open",
#            "resource_uri": "http://api.playwithlv.com/v1/leagues/6979/"
#        },
#        "league_id": 6979,
#        "leaguevine_url": "http://playwithlv.com/seasons/6980/club-open-2011/",
#        "name": "2011",
#        "resource_uri": "http://api.playwithlv.com/v1/seasons/6980/",
#        "start_date": "2011-01-01"
#    },
#    "season_id": 6980,
#    "start_date": "2012-06-15",
#    "swiss_pairing_type": "slide pairing",
#    "swiss_points_for_bye": "12.0",
#    "swiss_scoring_system": "victory points",
#    "timezone": "Europe/Amsterdam",
#    "uses_seeds": true,
#    "visibility": "hidden"
#}


CLIENT_ID='a18d62e40f4d269996b01f7cf462a9'
CLIENT_PWD='93dbb28011a5224303074b3deebaf6'
URL='http://playwithlv.com/oauth2/token/?client_id=a18d62e40f4d269996b01f7cf462a9&client_secret=93dbb28011a5224303074b3deebaf6&grant_type=client_credentials&scope=universal'

data=urllib2.urlopen(URL)

# parse string into Python dictionary
token=ast.literal_eval(data.read())
data.close()

SEASON_ID=6980

URL='http://api.playwithlv.com/v1/teams/?access_token=%s' % (token['access_token'])
print URL
    
req = urllib2.Request(url=URL)
req.add_header('Content-Type', 'application/json')
req.add_header('Accept', 'application/json')
req.add_header('Authorization', 'bearer %s' % (token['access_token']))

# create a new team with SEASON_ID
dict="{'name': '%s', 'season': '%d', 'info': '%s'}" % ("Test-Team", SEASON_ID, "test-info")
print dict
req.data=dict
f=urllib2.urlopen(req)
print f.read()
