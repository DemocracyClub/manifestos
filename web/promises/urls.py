from django.conf.urls.defaults import *
import views

urlpatterns = patterns('promises.views',
  url(r'^add_promises/$', 'add_promises', name='add_promises'),  
  url(r'^promises/$', 'all_promises', name='promises'),  
)
