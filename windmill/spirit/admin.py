from windmill.spirit.models import Game
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q

import logging

# Get an instance of a logger
logger = logging.getLogger('windmill.spirit')



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
        logger.info(request.GET['tournament_name'])
        if request.GET['tournament_name'] is not None:
            self.title=self.title+' in '+request.GET['tournament_name']
            qs=qs.filter(tournament_name=request.GET['tournament_name'])
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



class GameAdmin(admin.ModelAdmin):
    list_display = ['l_id','start_time','team_1_name','team_2_name','team_1_spirit','team_2_spirit']
    list_filter = ('tournament_name',EitherTeamListFilter)
    list_editable = ['team_1_spirit', 'team_2_spirit']

admin.site.register(Game, GameAdmin)
