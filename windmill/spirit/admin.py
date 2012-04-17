from windmill.spirit.models import Game
from django.contrib import admin

#class TeamAdmin(admin.ModelAdmin):
#    list_display = ['name', 'country', 'seed', 'tournament', 'l_id']
#    list_filter = ['tournament']
#    list_editable = ['seed']

class GameAdmin(admin.ModelAdmin):
    list_display = ['l_id','team1_id','team2_id']

admin.site.register(Game, GameAdmin)
