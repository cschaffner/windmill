from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from windmill.groupme.models import Message

import logging
from pprint import pformat

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')

@login_required
def overview(request):
    # GroupMe list all messages
    
    return render_to_response('groupme_overview.html')

def bot_callback(request):
    # receive POST request from GroupMe and save message in database
#     try:
    logger.info(pformat(request.POST))
    id = request.POST['id']
    user_id = request.POST['user_id']
    group_id = request.POST['group_id']
#     except:
    msg = Message.objects.create(id=id, user_id=user_id, group_id=group_id)

    return render_to_response('groupme_overview.html')
    