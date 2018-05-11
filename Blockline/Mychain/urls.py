from django.conf.urls import include, url
from django.views.generic import TemplateView
from Mychain import views
from Blockchains import chain


urlpatterns = [
    
    url(r'^test/(\d+)', views.test, name='test'),
    url(r'^testid' , views.testid, name='testid'),
    url(r'^connection/', TemplateView.as_view(template_name = 'login.html')),
    url(r'^login/', views.login, name='login'),

    
    
    # url(r'^$', TemplateView.as_view(template_name='index.html')),

    url(r'^$', views.mynode, name='home'),

    url(r'^mine/', chain.mine, name='mine'),

    url(r'^transaction/', chain.new_transactions, name='new_transactions'),
    
    url(r'^chain/', chain.full_chain , name='full_chain'),
    
    url(r'^nodes/register/', chain.register_nodes, name='register_node'),

    url(r'^nodes/resolve/', chain.consensus, name='resolve'),

    url(r'^data/', TemplateView.as_view(template_name = 'data.html'), name = 'data'),
     
    url(r'^register/', TemplateView.as_view(template_name = 'register.html'), name = 'register'),

    
   ]
