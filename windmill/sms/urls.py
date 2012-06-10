from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'windmill.views.home', name='home'),
    # url(r'^windmill/', include('windmill.foo.urls')),

    url(r'^$', 'windmill.sms.views.control'),
    url(r'^control$', 'windmill.sms.views.control'),
    url(r'^custom', 'windmill.sms.views.custom'),
    url(r'^submit$', 'windmill.sms.views.submit'),
    url(r'^status_update', 'windmill.sms.views.status_update'),
    
    url(r'^send', 'windmill.sms.views.send'),
    url(r'^logout$', 'windmill.sms.views.logout_view'),

    url(r'^create/(\d+)$', 'windmill.sms.views.create'),       
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
