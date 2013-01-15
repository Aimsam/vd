from django.conf.urls import patterns, include, url
from api.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$', hello),
    url(r'^love/(.*)', love),
    url(r'^get_list/$', get_list),
#    url(r'^/api/get_video/', hello),
#    url(r'^/api//', hello),
#    url(r'^/api/hello/', hello),
#    url(r'^/api/hello/', hello),
#    url(r'^/api/hello/', hello),
#    url(r'^/api/hello/', hello),
)
