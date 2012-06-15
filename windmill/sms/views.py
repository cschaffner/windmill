from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import datetime

from windmill.tools.wrapper import *
from windmill.spirit.models import Game
from windmill.tools.models import Team, Tournament
from windmill.sms.models import SMS
import logging
from pprint import pformat

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


@login_required
def control(request):
    # SMS control home
    SMStosend=SMS.objects.filter(status=u'ready')
    
    return render_to_response('sms_control.html',{'SMStosend': SMStosend, 'user': request.user},
                              context_instance=RequestContext(request))


@login_required
def status_sent(request):
    SMS.objects.change_status_to_sent()
    return HttpResponseRedirect(reverse('windmill.sms.control'))

def status_update(request):
    try:
        logger.info(pformat(request.GET))
        reference = request.GET['REFERENCE']
        status = request.GET['STATUS']
    except:
        logger.error('something went wrong while extracting information from GET body')
        return HttpResponse('<html>sms status update failed</html>')
    else:   
        sms=SMS.objects.get(id=reference)
        sms.status=status
        sms.receivedTime = datetime.datetime.now()
        sms.save()  
        return HttpResponse('<html>status updated</html>')
   

def send(request):
    # send SMS to Twilio here
    logger.info('we should send SMS to SmsCity here')
    message=SMS.objects.sendSmsCity()
    logger.info('message: {0}'.format(pformat(message)))
    return HttpResponseRedirect('control')

def custom(request):
    # create custom SMS to a specific team (or to all)
    return render_to_response('sms_custom.html', {'Teams': Team.objects.filter(seed__isnull=False).order_by('tournament','name')}, 
                              context_instance=RequestContext(request))

def submit(request):
    try:
        logger.info(pformat(request.POST))
        message = request.POST['txtMessage']
        target = request.POST.getlist('target')
        number = request.POST['number']
    except:
        return render_to_response('sms_custom.html', 
                                  {'error_message': 'the list of recipients was empty',
                                   'Teams': Team.objects.filter(seed__isnull=False).order_by('tournament','name')}, 
                                  context_instance=RequestContext(request))
    else:        
        if target==[] and number=='':
            return render_to_response('sms_custom.html', 
                          {'error_message': 'the list of recipients was empty',
                           'Teams': Team.objects.filter(seed__isnull=False).order_by('tournament','name')}, 
                          context_instance=RequestContext(request))
        if message=='':
            return render_to_response('sms_custom.html', 
                                      {'error_message': 'the message was empty',
                                       'Teams': Team.objects.filter(seed__isnull=False).order_by('tournament','name')}, 
                                      context_instance=RequestContext(request))

        logger.info('send message "{0}" to {1}'.format(message,pformat(target)))
        if target == 'broadcast':
            nr_created = SMS.objects.broadcast(message)
        elif number=='':
            nr_created = SMS.objects.sendSMS(message,target)
        elif target==[]:
            nr_created = SMS.objects.sendIndividualSMS(message,number)
        return HttpResponseRedirect('control')

def create(request,div):
    tournament=Tournament.objects.get(name=div)
    
    # retrieve tournament info
    if settings.OFFLINE:
        t={u'info': u'', u'swiss_victory_points_cap': 23, u'name': u'Windmill Windup Test (open)', u'end_date': u'2012-06-16', u'season': {u'league': {u'leaguevine_url': u'http://playwithlv.com/leagues/6979/club-open/', u'id': 6979, u'resource_uri': u'http://api.playwithlv.com/v1/leagues/6979/', u'name': u'Club Open'}, u'name': u'2011', u'end_date': u'2011-12-31', u'league_id': 6979, u'time_created': u'2011-02-17T08:14:44+00:00', u'start_date': u'2011-01-01', u'leaguevine_url': u'http://playwithlv.com/seasons/6980/club-open-2011/', u'time_last_updated': u'2011-02-17T08:14:44+00:00', u'id': 6980, u'resource_uri': u'http://api.playwithlv.com/v1/seasons/6980/'}, u'swiss_victory_points_games_to': 13, u'time_created': u'2012-04-15T20:37:20+00:00', u'scheduling_format': u'swiss', u'season_id': 6980, u'timezone': u'US/Central', u'leaguevine_url': u'http://playwithlv.com/tournaments/18055/windmill-windup-test-open/', u'swiss_points_for_bye': u'1.0', u'start_date': u'2012-06-14', u'swiss_scoring_system': u'victory points', u'swiss_pairing_type': u'adjacent pairing', u'visibility': u'live', u'number_of_sets': None, u'time_last_updated': u'2012-04-15T20:37:20+00:00', u'uses_seeds': True, u'id': 18055, u'resource_uri': u'http://api.playwithlv.com/v1/tournaments/18055/'}
    else:
        t=api_tournamentbyid(tournament.lgv_id())
    logger.info(t)
    # check if there are playoff rounds
    # if yes, load them in brackets
    brackets=api_bracketsbytournament(tournament.lgv_id())
    if t['scheduling_format']=='swiss':
        if settings.OFFLINE==True:
            swiss=swissinfo()
        else:
            swiss=api_swissroundinfo(tournament.lgv_id())
#        logger.info(pformat(swiss))
        if not request.GET.__contains__('round'):
            # display choice of rounds
            return render_to_response('sms_selectround.html',{'tournament': t, 'swiss': swiss, 'brackets': brackets})
        else:
            selround=request.GET['round']
            if selround=='QF' or selround=='SF' or selround=='F' or selround=='afterF':
                nr_created=SMS.objects.bracket_round(brackets,swiss,selround,t)
            else:
                round_nr = int(selround)
                if not round_nr > 0:
                    raise 'something is wrong with the round argument'
                nr_created=SMS.objects.swiss_round(swiss,round_nr,t)
        
    elif t['scheduling_format']=='regular':
        # do something here
        logger.error('treat regular format here')
    
    # SMS control home
    SMStosend=SMS.objects.filter(status=u'ready')
    
    return render_to_response('sms_control.html',{'nr_created': nr_created, 'SMStosend': SMStosend, 'user': request.user},
                              context_instance=RequestContext(request))
    

def logout_view(request):
    logout(request)
    # Redirect to login via control
    return render_to_response('sms_logout_success.html')

@login_required
def phonenumbers(request):
    # display phone numbers of all teams
    teams = Team.objects.order_by('tournament','name')
    return render_to_response('sms_phonenumbers.html', {'teams': teams})

