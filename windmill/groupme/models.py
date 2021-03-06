from django.db import models

# class GroupMe_Manager(models.Manager):
#     def change_status_to_sent(self):
#         SendList = SMS.objects.filter(status=u'ready')
#         for sms in SendList:
#             sms.status="sent"
#             sms.save()
#         return 
    
class Message(models.Model):
#     objects = GroupMe_Manager()
    msg_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.BigIntegerField(null=True, blank=True)
    user_id = models.CharField(max_length=20, null=True, blank=True)
    group_id = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    text = models.CharField(max_length=200, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    post_string = models.CharField(max_length=500, blank=True, null=True)
    
    def __unicode__(self):
        return '{0}: {1}'.format(self.name,self.text)

    
