from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'windmill.views.home', name='home'),
    # url(r'^windmill/', include('windmill.foo.urls')),

    url(r'^$', 'windmill.powerrank.views.home'),
    url(r'^addtournament/(\d+)$', 'windmill.powerrank.views.addtournament'),  
    url(r'^power/(\d+)$', 'windmill.powerrank.views.power'),  
             
#    url(r'^update/$', 'windmill.powerrank.views.update'),       
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
