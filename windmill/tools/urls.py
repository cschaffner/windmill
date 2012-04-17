from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'windmill.views.home', name='home'),
    # url(r'^windmill/', include('windmill.foo.urls')),

    url(r'^$', 'windmill.tools.views.home'),
    url(r'^(open|mixed|women)/division/$', 'windmill.tools.views.division'),       
    url(r'^(open|mixed|women)/addteams/$', 'windmill.tools.views.addteams'),   
    url(r'^(open|mixed|women)/newtourney/$', 'windmill.tools.views.newtourney'),    
    url(r'^(open|mixed|women)/clean$', 'windmill.tools.views.clean'),
    url(r'^(open|mixed)/addswissround$', 'windmill.tools.views.addswissround'),
    url(r'^(women)/addpools$', 'windmill.tools.views.addpools'),
    url(r'^(open|mixed|women)/randomresults$', 'windmill.tools.views.randomresults'),

    url(r'^createteams/$', 'windmill.tools.views.createteams'),   
    url(r'^import$', 'windmill.tools.views.ffimport'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)