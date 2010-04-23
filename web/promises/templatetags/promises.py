from django.contrib.contenttypes.models import ContentType
from django.template import Library, Node

register = Library()

@register.inclusion_tag('add_promise.html', takes_context=True)
def add_promise(context, promise_object):
    ct = ContentType.objects.get_for_model(promise_object)
    
    return {
    'ct' : ct,
    'promise_object' : promise_object,
    }
