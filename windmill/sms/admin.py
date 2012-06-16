from windmill.sms.models import Tournament, SMS, SMSOverview
from django.contrib import admin

import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')


class SMSAdmin(admin.ModelAdmin):
    list_display = ['id','team','tournament','round_id','createTime','number','message','length','status']
    list_filter = ('tournament','team','round_id','status')
#    list_editable = ['status']



class SMSOverviewAdmin(admin.ModelAdmin):
    list_display = ['id','createTime','receivedTime','team','number','length','status']
    list_filter = ('tournament','team','round_id','status')

admin.site.register(SMS, SMSAdmin)
admin.site.register(SMSOverview, SMSOverviewAdmin)
