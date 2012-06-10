from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'windmill.views.home', name='home'),
    # url(r'^windmill/', include('leaguevine.foo.urls')),

    url(r'^tools/', include('windmill.tools.urls')),
    url(r'^spirit/', include('windmill.spirit.urls')),
    url(r'^sms/', include('windmill.sms.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login')
    
 )
