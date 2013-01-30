from django.conf.urls import patterns, include, url
from api.views import *
import views,os
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^love/(.*)', love),
    url(r'^get_list/$', get_list),
    url(r'^aaa/$', views.index),
    url(r'^js/(.*)$','django.views.static.serve',
        {'document_root':os.path.dirname(__file__)+'/js_css/'}
    ),
    url(r'^css/(.*)$','django.views.static.serve',
        {'document_root':os.path.dirname(__file__)+'/js_css/'}
    ),
#    url(r'^/api/get_video/', hello),
#    url(r'^/api//', hello),
#    url(r'^/api/hello/', hello),
#    url(r'^/api/hello/', hello),
#    url(r'^/api/hello/', hello),
#    url(r'^/api/hello/', hello),
)
