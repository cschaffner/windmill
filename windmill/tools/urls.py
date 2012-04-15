from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'leaguevine.views.home', name='home'),
    # url(r'^leaguevine/', include('leaguevine.foo.urls')),

    url(r'^$', 'addons.views.home'),
    url(r'^(open|mixed|women)/division/$', 'addons.views.division'),       
    url(r'^(open|mixed|women)/addteams/$', 'addons.views.addteams'),   
    url(r'^(open|mixed|women)/newtourney/$', 'addons.views.newtourney'),    
    url(r'^(open|mixed|women)/clean$', 'addons.views.clean'),
    url(r'^(open|mixed)/addswissround$', 'addons.views.addswissround'),
    url(r'^(women)/addpools$', 'addons.views.addpools'),
    url(r'^(open|mixed|women)/randomresults$', 'addons.views.randomresults'),

    url(r'^createteams/$', 'addons.views.createteams'),   
    url(r'^import$', 'addons.views.ffimport'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
