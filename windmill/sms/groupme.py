## this module interacts with the GroupMe API
## http://dev.groupme.com/docs/v3

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

access_token = '45a4ade03b360130444a1231381565ac'

if access_token == None:
    # Make a request for an access_token
    if settings.OFFLINE:
        access_token='offline'
    else:
        url=u'{0}/oauth2/token/?client_id={1}&client_secret={2}&grant_type=client_credentials&scope=universal'.format(settings.TOKEN_URL, settings.CLIENT_ID, settings.CLIENT_PWD)
        r=requests.get(url)
        # parse string into Python dictionary
        r_dict = simplejson.loads(r.content)
        access_token = r_dict.get('access_token')
        cache.set('access_token', access_token)
        logger.info('retrieved a new access token: {0}'.format(access_token))
            
GROUPME='https://api.groupme.com/v3'
my_headers={'User-Agent': 'Windmill Windup 2013 Notifications', 'Accept': '*/*', 'X-Access-Token': '{0}'.format(access_token)}  
my_config={'verbose': sys.stderr}

def api_post(url,dict):
    # does a POST on url, sending dict
    datastring=json.dumps(dict)
    logger.info(datastring)
    response=requests.post(url=url,headers=my_headers,config=my_config,data=datastring)
    if response.status_code == 400: # what's that?
        logger.error(response.text)
        response.raise_for_status
    elif response.status_code>202: # if not "created"
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

def api_update(url,updatedict={}):
    # first retrieves the data of an object
    # then merges the fields with updatedict
    # and PUTs it again
    # works e.g. for tournaments and games

    response = requests.get(url=url,headers=my_headers,config=my_config)
    response_dict = simplejson.loads(response.content)
    
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
  
 
def api_getgroups():
    url='{0}/groups'.format(GROUPME)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    logger.info(response.content)
    response_dict = simplejson.loads(response.content)
    return response_dict

def api_getbots():
    url='{0}/bots'.format(GROUPME)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    if response.status_code == 404: # what's that?
        logger.error(response.text)
        response.raise_for_status
    else:
        response_dict = simplejson.loads(response.content)
        return response_dict

def api_createbot(name,group_id):
    url='{0}/bots'.format(GROUPME)
    data={u'name': name,
          u'group_id': group_id}
#    ,
#          u'bot[group_id]': u'3310910',
#          u'callback_url': u'http://www.windmill.com/2013/bot_callback'}
    return api_post(url,data)

def api_creategroup(name):
    url='{0}/groups'.format(GROUPME)
    data={u'name': name}
    return api_post(url,data)

def api_addmembers(group_id):
    url='{0}/groups/{1}/members/add'.format(GROUPME,group_id)
    data={'members': [{'nickname': 'Chris Fon',
                       'phone_number': '+31 619091702'},
                      {'nickname': 'Chris Email',
                       'email': 'cschaffner@mcsoftware.ch'}]}
    return api_post(url,data)

