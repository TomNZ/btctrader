from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Trader
urlpatterns = patterns(
    'trader.views',
    url(r'^/?$', 'index', name='index'),
    url(r'^market/(?P<market_id>\d+)/?$', 'market_view', name='market_view'),
    url(r'^dashboard/?$', 'dashboard', name='dashboard'),
)

# Trader API
urlpatterns += patterns(
    'trader.views',
    url(r'^order/submit/?$', 'order_submit', name='order_submit'),
)

# Admin
urlpatterns += patterns(
    '',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
