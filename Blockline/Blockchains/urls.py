"""
Definition of urls for Blockchain.
"""

from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin
from Blockchains import chain
import sys
sys.path.insert(0,'Mychain/scripts')
import rd, coins

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^$', coins.show_coin , name = 'index'),
    
    url(r'^mynode/',include('Mychain.urls'), name = 'links'),
    
    url(r'^rate_difference/$', rd.view_rd , name= 'rd' ),

    url(r'^rate_difference/(?P<ex>[a-z])/$', rd.view_rd , name= 'rd' ),
    

 
    ]