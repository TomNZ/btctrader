from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Trader
urlpatterns = patterns('trader.views',
    url(r'^/?$', 'index', name='index'),
    url(r'^market/(?P<market_id>\d+)/?$', 'market_view', name='market_view'),
)

# Admin
urlpatterns += patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
