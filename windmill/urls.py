from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'windmill.views.home', name='home'),
    # url(r'^windmill/', include('leaguevine.foo.urls')),

    url(r'^tools/', include('windmill.tools.urls')),
    
 )
