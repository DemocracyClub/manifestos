from django.conf.urls.defaults import *
import views

urlpatterns = patterns('documents.views',
  url(r'^$', 'documents', name='documents'),  
  url(r'^(?P<docid>\d)/$', 'document', name='document'),
  url(r'^(?P<docid>\d+)/browse/(?P<elid>\d+)/$', 'element', name='element'),
  url(r'^add_tag/$', 'add_tag', name='add_tag'),
  url(r'^search/$', 'search', name='search'),
  url(r'^search/(?P<query>.*)/$', 'search', name='search'),
)