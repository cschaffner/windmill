from windmill.powerrank.models import Tournament, Game, Team, Round, Standing
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django import forms

import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.powerrank')



class EitherTeamListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('teams')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'team'

    def lookups(self, request, model_admin):
        from itertools import chain
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        qs = model_admin.queryset(request)
        logger.info(qs)
        if request.GET.__contains__('tournament__id__exact'):
            logger.info(request.GET['tournament__id__exact'])
            self.title=self.title+' in '+Tournament.objects.get(id=request.GET['tournament__id__exact']).name
            qs=qs.filter(tournament=request.GET['tournament__id__exact'])
        team1list=qs.order_by('team_1_name').distinct('team_1_name').values_list('team_1_name','team_1_name')
        team2list=qs.order_by('team_2_name').distinct('team_2_name').values_list('team_2_name','team_2_name')
        teamlist=sorted(list(set(chain(team1list,team2list))))
        return teamlist

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        logger.info(u'self.value() = {0}'.format(self.value()))
        if self.value() is None:
            return queryset
        else:
            return queryset.filter(Q(team_1_name=self.value()) | Q(team_2_name=self.value()))

class MyGameAdminForm(forms.ModelForm):
    class Meta:
        model = Game
        
    def clean_name(self):
        return self.cleaned_data['name']


class GameAdmin(admin.ModelAdmin):
    list_display = ['l_id','lv_id','start_time','team_1','team_2','team_1_score','team_2_score']
    list_filter = ('round',)
#    list_filter = ('round',EitherTeamListFilter)
    form = MyGameAdminForm

class TeamAdmin(admin.ModelAdmin):
    list_display = ['l_id','lv_id','name']

class StandingAdmin(admin.ModelAdmin):
    list_display = ['team','round','wins','losses','swiss_rank', 'swiss_score']
    list_filter = ('team','round')


admin.site.register(Tournament)
admin.site.register(Game, GameAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Round)
admin.site.register(Standing, StandingAdmin)
