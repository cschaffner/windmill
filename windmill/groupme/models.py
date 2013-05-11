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
    id = models.CharField(primary_key=True, max_length=50)
    created_at = models.IntegerField(null=True, blank=True)
    user_id = models.CharField(max_length=20, null=True, blank=True)
    group_id = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    text = models.CharField(max_length=200, blank=True, null=True)
    
