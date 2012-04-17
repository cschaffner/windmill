from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.conf import settings
import windmill.tools.wrapper
from windmill.spirit.models import Game
import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


def home(request):
    return render_to_response('spirit.html',{'Games': Game.objects.all})
