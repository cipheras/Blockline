"""
Definition of urls for Blockchain.
"""

from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib import admin
from Blockchain import chain
import sys
sys.path.insert(0,'MychainApp/scripts')
import rd, coins

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^$', coins.show_coin , name = 'index'),
    
    url(r'^mynode/',include('MychainApp.urls'), name = 'links'),
    
    url(r'^api/rate_difference/$', rd.api_rd , name= 'rd' ),

    url(r'^api/rate_difference/(?P<ex>[a-z])/$', rd.api_rd , name= 'rd' ),

    url(r'^api/rate_difference/(?P<ex>[a-z])/(?P<mk>btc|inr)/$', rd.api_rd , name= 'rd' ),
    
   
    
    ]