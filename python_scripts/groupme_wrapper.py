## this module interacts with the GroupMe API
## http://dev.groupme.com/docs/v3

# from django.utils import simplejson
# from django.conf import settings
# from django.core.cache import cache
import requests
import logging
import sys
import csv
import itertools
import json
from pprint import pformat
import os

# create logger with 'spam_application'
logger = logging.getLogger('my_logger')


ROOT_PATH = os.path.dirname(__file__)
OFFLINE = False

# expects credentials to be stored in environmental variables!

access_token = os.environ['GROUPME_TOKEN']

if access_token == None:
    # Make a request for an access_token
    if settings.OFFLINE:
        access_token='offline'
    else:
        url=u'{0}/oauth2/token/?client_id={1}&client_secret={2}&grant_type=client_credentials&scope=universal'.format(settings.TOKEN_URL, settings.CLIENT_ID, settings.CLIENT_PWD)
        r=requests.get(url)
        # parse string into Python dictionary
        r_dict = json.loads(r.content)
        access_token = r_dict.get('access_token')
        cache.set('access_token', access_token)
        logger.info('retrieved a new access token: {0}'.format(access_token))
            
GROUPME='https://api.groupme.com/v3'
GROUPMEv2='https://v2.groupme.com'
my_headers={'User-Agent': 'Windmill Windup 2013 Testing', 'Accept': '*/*', 'X-Access-Token': '{0}'.format(access_token)}  
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
    elif response.status_code == 202:
        logger.info('POST request accepted')
        return True        
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
  
 
def api_get_groups():
    url='{0}/groups'.format(GROUPME)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    logger.info(response.content)
    response_dict = json.loads(response.content)
    return response_dict

def api_get_bots():
    url='{0}/bots'.format(GROUPME)
    response = requests.get(url=url,headers=my_headers,config=my_config)
    if response.status_code == 404: # what's that?
        logger.error(response.text)
        response.raise_for_status
    else:
        response_dict = json.loads(response.content)
        return response_dict

def api_create_bot(name, group_id, avatar_url=None, callback_url=None):
    url='{0}/bots'.format(GROUPME)
    data={'bot': {u'name': name,
                  u'group_id': group_id}}
    if avatar_url:
        data[u'avatar_url'] =  avatar_url
    if callback_url:
        data[u'callback_url'] = callback_url
    return api_post(url,data)

def api_submit_group(name):
    groups = api_get_groups()
    for g in groups['response']:
        if g['name'] == name:
            return g
    description = u'Group for Windmill Windup 2013 to receive team notifications. Further information on http://www.windmillwindup.com'
    image_url = u'http://i.groupme.com/a54d607094860130d3121234e284d7b4'
    response = api_create_group(name, description, image_url, True)
    if response['meta']['code'] == 201:
        return response['response']
    else:
        raise

def api_create_group(name, description=None, image_url=None, share=False):
    url = '{0}/groups'.format(GROUPME)
    data = {u'name': name}
    if description:
        data[u'description'] = description
    if image_url:
        data[u'image_url'] = image_url
    data['share'] = share    
    return api_post(url, data)

def api_change_group(group_id, name=None, description=None, image_url=None, share=False):
    url = '{0}/groups/{1}/update'.format(GROUPME, group_id)
    data = {}
    if name:
        data[u'name'] = name
    if description:
        data[u'description'] = description
    if image_url:
        data[u'image_url'] = image_url
    data[u'share'] = share
    return api_post(url, data)

def api_add_members(group_id):
    url='{0}/groups/{1}/members/add'.format(GROUPME,group_id)
    data={'members': [{'nickname': 'Les',
                       'email': '+31 626072266'},
                      {'nickname': 'Fred',
                       'email': '+31 614189776'}]}
    return api_post(url,data)

def api_send_message(group_id,msg,location=''):
    url='{0}/groups/{1}/messages'.format(GROUPMEv2,group_id)
    data={'message': {'source_guid': 'GUID',
                      'text': msg}}
    if not location=='':
        data['message']['location']=location
    return api_post(url,data)
