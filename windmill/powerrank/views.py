from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from windmill.powerrank.models import Tournament
import logging
from pprint import pformat

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


def home(request):
    # refer to admin interface 
    return render_to_response('powerrank.html',{'added': 0})

def addtournament(request,tournament_id):
    Tournament.objects.add(tournament_id)
    return HttpResponseRedirect('/')
