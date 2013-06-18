from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zhutao.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'payment.views.index', name="index"),
    url(r'^return/$', 'payment.views.return_', name="return"),
    url(r'^cancel/$', 'payment.views.cancel', name="cancel"),
    url(r'^notify/$', 'payment.views.notify', name="notify"),
    url(r'^__paypal/', include('paypal.digitalgoods.urls')),
)
