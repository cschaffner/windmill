from windmill.tools.models import Tournament, Team, TeamPhone
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'country_code', 'seed', 'tournament', 'l_id','lv_id']
    list_filter = ['tournament']
    list_editable = ['seed']


class TeamPhoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'country_code', 'mobile1', 'mobile2', 'mobile3', 'mobile4', 'mobile5']
    list_filter = ['tournament']
    list_editable = ['mobile1', 'mobile2', 'mobile3', 'mobile4', 'mobile5']


class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'l_id','lv_id']

admin.site.register(Team, TeamAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TeamPhone, TeamPhoneAdmin)

admin.site.register(ContentType)
admin.site.register(Permission)