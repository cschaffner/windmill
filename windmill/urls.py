from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'windmill.views.home', name='home'),
    # url(r'^windmill/', include('leaguevine.foo.urls')),

    url(r'^tools/', include('windmill.tools.urls')),
    url(r'^spirit/', include('windmill.spirit.urls')),
    url(r'^sms/', include('windmill.sms.urls')),
    url(r'^powerrank/', include('windmill.powerrank.urls')),
    url(r'^groupme/', include('windmill.groupme.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login')
    
 )

urlpatterns += staticfiles_urlpatterns()
