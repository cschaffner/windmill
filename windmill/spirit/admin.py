from windmill.spirit.models import Game
from django.contrib import admin

#class TeamAdmin(admin.ModelAdmin):
#    list_display = ['name', 'country', 'seed', 'tournament', 'l_id']
#    list_filter = ['tournament']
#    list_editable = ['seed']

class GameAdmin(admin.ModelAdmin):
    list_display = ['l_id','start_time','team_1_name','team_2_name','team_1_spirit','team_2_spirit']
    list_filter = ['tournament_name']
    list_editable = ['team_1_spirit', 'team_2_spirit']

admin.site.register(Game, GameAdmin)
