from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from windmill.tools.wrapper import *
from windmill.spirit.models import Game
from windmill.sms.models import SMS
import logging
from pprint import pformat

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')

"""
GOAL: 

Swissdraw:
$text = "Welcome to Windmill Windup 2012!In round 1,";

// After a 15-2 loss in round 1, you are now ranked 12th. In round 2,
// you'll play "Ultimate Kaese" (ranked 13th) on Field 1 at 12:30.

Brackets:
// After a 15-10 win in round 5, your final rank after Swissdraw is 25th. You will thus play for rank 1 to 8.
// In the quarter finals, you'll play CamboCakes (ranked 5th) on Field 10. Pls handin today's spirit scores.

// After a 15-2 loss in the quarter finals, you'll play the semi finals against
// "Ultimate Kaese" (Swiss-ranked 13th) on Field 1 at 12:30.

// After a 15-2 loss in the semi finals, 
// you'll play for 9th against "Ultimate Kaese" (Swiss-ranked 13th) on Field 1 at 12:30.
// or: you finish Windmill 2011 in place 18.

// After a 15-2 loss in the final game, you finish Windmill 2010 in place 1. Congratulations!
// Please hand in today's spirit scores and see you next year!
        
// After a 13-12 win in the exciting final, you are the champion of Windmill 2010. Congratulations!"
// After a 11-18 loss in the final, you are vice-champion of Windmill 2010. Congratulations!"
"""

def home(request):
    # SMS control home
    return render_to_response('sms_control.html')

def control(request):
    # SMS control home
    return render_to_response('sms_control.html')

def broadcast(request):
    return render_to_response('sms_broadcast.html', context_instance=RequestContext(request))

def submit(request):
    try:
        logger.info(pformat(request.POST))
        message = request.POST['message']
    except (KeyError, Message.DoesNotExist):
        return render_to_response('sms_broadcast.html', {'error_message': 'your message was empty'}, 
                                  context_instace=RequestContext(request))
    else:        
        logger.info('send message "{0}" to everybody'.format(message))
        SMS.objects.broadcast(message)
        return HttpResponseRedirect('control')

def create(request,tournament_id):
    # retrieve tournament info
    t=api_tournamentbyid(tournament_id)
    if t['scheduling_format']=='swiss':
        swiss=api_swissroundinfo(tournament_id)
        
    elif t['scheduling_format']=='regular':
        # do something here
        logger.error('treat regular format here')
    

    
    
