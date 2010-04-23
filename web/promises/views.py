from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404



from models import Promise

def add_promises(request):
    if request.POST:
        content_type = request.POST.get('content_type')
        object_id = request.POST.get('object_id')
        
        ct = ContentType.objects.get(name=content_type)
        
        
        p = Promise(content_type=ct, object_id=object_id)
        p.save()

    return HttpResponseRedirect("%s#%s" % (request.META['HTTP_REFERER'], object_id))



def all_promises(request):
    promises = Promise.objects.all()
    
    print promises[0].content_object.get_parent()
    
    return render_to_response(
      'promises.html', 
      {
      'promises' : promises,
      },
      context_instance=RequestContext(request)
    )  
    