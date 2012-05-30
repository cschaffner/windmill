from windmill.sms.models import Tournament, SMS
from django.contrib import admin

import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


class SMSAdmin(admin.ModelAdmin):
    list_display = ['id','team','tournament','round_id','number','message','status']
    list_filter = ('tournament','team','round_id')

admin.site.register(SMS, SMSAdmin)
