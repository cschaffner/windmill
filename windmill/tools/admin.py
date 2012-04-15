from addons.models import Tournament, Team
from django.contrib import admin

class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'seed', 'tournament', 'l_id']
    list_filter = ['tournament']
    list_editable = ['seed']

class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'l_id']

admin.site.register(Team, TeamAdmin)
admin.site.register(Tournament, TournamentAdmin)
