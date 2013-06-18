from django.conf.urls.defaults import *

urlpatterns = patterns('paypal.digitalgoods.views',            
    url(r'^dg/$', 'dg', name="paypal-dg"),
)
