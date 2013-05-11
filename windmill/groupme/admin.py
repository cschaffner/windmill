from windmill.groupme.models import Message
from django.contrib import admin

import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')

 
class MessageAdmin(admin.ModelAdmin):
    list_display = ['group_id','created_at','name','text']
    list_filter = ('group_id',)
#    list_editable = ['status']
# 
# 
# 
# class SMSOverviewAdmin(admin.ModelAdmin):
#     list_display = ['id','createTime','receivedTime','team','number','length','status']
#     list_filter = ('tournament','team','round_id','status')

admin.site.register(Message, MessageAdmin)
