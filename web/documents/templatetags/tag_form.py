from django.template import Library, Node
from django.template import Context, Variable
from documents import forms
register = Library()


@register.inclusion_tag('includes/add_tag.html', takes_context=True)
def add_tag(context, element):
    form = forms.TagForm()
    
    return {
        'form' : form,
        'element' : element,
    }
