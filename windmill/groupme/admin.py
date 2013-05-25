from windmill.groupme.models import Message
from django.contrib import admin

import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')

def team_name(obj):
    
    team_dict = {u'4410557': u'Southern Skies',
                 u'4410558': u'Funatics',
                 u'4410559': u'Frank N',
                 u'4410560': u'Bad Skid',
                 u'4410561': u'Iznogood',
                 u'4410562': u'Chiniya Rada',
                 u'4410564': u'Ka-pow!',
                 u'4410565': u'Ragnarok',
                 u'4410566': u'FUJ',
                 u'4410567': u'Freespeed',
                 u'4410568': u'Wall City Berlin',
                 u'4410569': u'Rebel Ultimate',
                 u'4410571': u'Mor ho!',
                 u'4410572': u'Flying Steps Frisbee Club',
                 u'4410573': u'Crazy Dogs Stans',
                 u'4410574': u'Blue Arse Flies',
                 u'4410575': u'Broc Ultimate',
                 u'4410576': u'Heidees',
                 u'4410577': u'TheBigEz',
                 u'4410580': u'Women on Fire',
                 u'4410581': u'Lemon Grass',
                 u'4410583': u'Germany U20 Women',
                 u'4410584': u'Eyecatchers',
                 u'4410585': u'Lotus Switzerland',
                 u'4410587': u'Hot Beaches',
                 u'4410588': u'CUSB LA FOTTA Under 23',
                 u'4410589': u'JinX',
                 u'4410591': u'Up!',
                 u'4410592': u'Woodchicas',
                 u'4410593': u"Lay D's",
                 u'4410594': u'Frizzly Bears',
                 u'4410595': u'Heidees Damen',
                 u'4410597': u'U de Cologne',
                 u'4410598': u'CUSB women',
                 u'4410601': u'Copenhagen Hucks',
                 u'4410602': u'Purple Rhino',
                 u'4410603': u'Seagulls',
                 u'4410605': u'Sun Cr\xe9teil',
                 u'4410606': u'Sexy Legs',
                 u'4410607': u'Headless Ultimate Z\xfcrich',
                 u'4410608': u'Hardfisch',
                 u'4410609': u'Germany Junior Open',
                 u'4410610': u'Ireland Under 23 Mixed',
                 u'4410612': u"Father Abraham's soup of the day",
                 u'4410614': u'Prague Devils',
                 u'4410616': u'Israel Mix',
                 u'4410618': u'UFO (Utrecht)',
                 u'4410619': u'Catchup Graz',
                 u'4410620': u'Outernationals',
                 u'4410621': u'Wombat Ultimate Willisau',
                 u'4410622': u'Aye-Aye Ultimate (UEA)',
                 u'4410623': u'LuckyGrass',
                 u'4410624': u'Gentle Open',
                 u'4410626': u'PUF',
                 u'4410627': u'Gronical Dizziness',
                 u'4410628': u'Thundering Herd',
                 u'4410629': u'Mubidisk Lanzarote',
                 u'4410630': u'Quijotes+Dulcineas Ultimate Madrid',
                 u'4410631': u'Mooncatchers',
                 u'4410632': u'Star Spangled Hammers',
                 u'4410633': u'Cambo Cakes',
                 u'4410634': u'KFK Copenhagen',
                 u'4410635': u'Israel Open',
                 u'4410636': u'Deine Mudder Bremen',
                 u'4410638': u'Happy Hour',
                 u'4410639': u'Fizzy Lifting Drinks',
                 u'4410640': u'Uprising',
                 u'4410641': u'Rebel Ultimate',
                 u'4410642': u'7 Schwaben',
                 u'4410643': u'Rusty Bikes',
                 u'4410644': u'Breizh United',
                 u'4410645': u'UL Ninjas',
                 u'4410646': u'Flying Bisc',
                 u'4410647': u'Germany U23 Mixed',
                 u'4410649': u'UFO (Utrecht)',
                 u'4410650': u'Stockholm Syndromes',
                 u'4410651': u'Friselis Versailles',
                 u'4410652': u'Cranberry Snack',
                 u'4410653': u'M.U.C.',
                 u'4410654': u'Good Lord!'}
    return team_dict[obj]

team_name.short_description = 'Team name'

 
class MessageAdmin(admin.ModelAdmin):
    list_display = [team_name,'created_at','name','text']
    list_filter = ('group_id',)
#    list_editable = ['status']
# 
# 
# 
# class SMSOverviewAdmin(admin.ModelAdmin):
#     list_display = ['id','createTime','receivedTime','team','number','length','status']
#     list_filter = ('tournament','team','round_id','status')

admin.site.register(Message, MessageAdmin)
