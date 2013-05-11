from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt                                          
from windmill.groupme.models import Message

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
#         id = request.POST['id']
#         user_id = request.POST['user_id']
#         group_id = request.POST['group_id']
#         msg = Message.objects.create(id=id, user_id=user_id, group_id=group_id)
#         msg.save()

    return render_to_response('groupme_overview.html')
    