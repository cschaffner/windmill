from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'leaguevine.views.home', name='home'),
    # url(r'^leaguevine/', include('leaguevine.foo.urls')),

    url(r'^tools/', include('tools.urls')),
    
 )
