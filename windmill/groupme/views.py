from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt                                          
from windmill.groupme.models import Message
import json

import logging
from pprint import pformat

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')

@login_required
def overview(request):
    # GroupMe list all messages
    
    return render_to_response('groupme_overview.html')

@csrf_exempt                                                                                  
def bot_callback(request):
    # receive POST request from GroupMe and save message in database
#     try:
    if request.method == "POST":
        logger.info(pformat(request.POST))
        post_list = request.POST.items()
        dict = json.loads(post_list[0][0])
                     
        msg = Message.objects.create(msg_id = dict['id'], 
                                     user_id = dict['user_id'], 
                                     group_id = dict['group_id'],
                                     created_at = dict['created_at'],
                                     name = dict['name'],
                                     text = dict['text'],
                                     post_string = post_list[0][0])
        msg.save()
# 
# {u'{"id":"136830022150627694",
#     "source_guid":"ios389993017.89447503CAAAC1-8A3D-43DF-B139-12EA1EAC809E",
#     "created_at":1368300221,
#     "user_id":"8521911",
#     "group_id":"4410557",
#     "name":"Chris",
#     "avatar_url":null,
#     "text":"Hello Herbie!",
#     "system":false,
#     "attachments":[]}': [u'']}

    return render_to_response('groupme_overview.html')
    