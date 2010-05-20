from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

from models import Document, Element
from forms import SearchForm
from index import ElementIndexer
import xapian

def documents(request):
    docs = Document.objects.all()
    return render_to_response(
      'documents.html', 
      {
      'docs' : docs,
      },
      context_instance=RequestContext(request)
    )  

def document(request, docid):
    doc = get_object_or_404(Document, pk=docid)
    headings = Element.objects.filter(document=doc, tag='h1')
    return render_to_response(
      'document.html', 
      {
      'doc' : doc,
      'headings' : headings,
      },
      context_instance=RequestContext(request)
    )  

def element(request, docid, elid):
    doc = get_object_or_404(Document, pk=docid)
    element = get_object_or_404(Element, pk=elid)

    return render_to_response(
      'element.html', 
      {
      'doc' : doc,
      'element' : element,
      },
      context_instance=RequestContext(request)
    )  


def add_tag(request):
    if not request.POST:
        return HttpResponseRedirect('/')
    
    element = Element.objects.get(pk=request.POST.get('element'))
    element.tags.add(request.POST.get('tags'))
    element.save()
    print request.META['HTTP_REFERER']
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    
def search(request, query=None):
    results = None
    coalition_results = green_results = libdem_results = labour_results = tory_results, coalition_final_results = None
    if request.POST:
        q = request.POST.get('q')
        return HttpResponseRedirect(reverse('search', args=[q]))

    if query:
        form = SearchForm(data={'q' : query})

        q = query
        indexer = Element.indexer
        libdem_results = indexer.search("%s party:libdem" % q)
        coalition_results = indexer.search("%s party:coalitiona" % q)
        coalition_final_results = indexer.search("%s party:coalition_final" % q)
        green_results = indexer.search("%s party:green" % q)
        labour_results = indexer.search("%s party:labour" % q)
        tory_results = indexer.search("%s party:tory" % q)

        coalition_results=coalition_results.flags(xapian.QueryParser.FLAG_PHRASE\
                        | xapian.QueryParser.FLAG_BOOLEAN\
                        | xapian.QueryParser.FLAG_LOVEHATE
                        | xapian.QueryParser.FLAG_WILDCARD
                        )
        coalition_final_results=coalition_final_results.flags(xapian.QueryParser.FLAG_PHRASE\
                        | xapian.QueryParser.FLAG_BOOLEAN\
                        | xapian.QueryParser.FLAG_LOVEHATE
                        | xapian.QueryParser.FLAG_WILDCARD
                        )
        green_results=green_results.flags(xapian.QueryParser.FLAG_PHRASE\
                        | xapian.QueryParser.FLAG_BOOLEAN\
                        | xapian.QueryParser.FLAG_LOVEHATE
                        | xapian.QueryParser.FLAG_WILDCARD
                        )
        labour_results=labour_results.flags(xapian.QueryParser.FLAG_PHRASE\
                        | xapian.QueryParser.FLAG_BOOLEAN\
                        | xapian.QueryParser.FLAG_LOVEHATE
                        | xapian.QueryParser.FLAG_WILDCARD
                        )
        libdem_results=libdem_results.flags(xapian.QueryParser.FLAG_PHRASE\
                        | xapian.QueryParser.FLAG_BOOLEAN\
                        | xapian.QueryParser.FLAG_LOVEHATE
                        | xapian.QueryParser.FLAG_WILDCARD
                        )
        tory_results=tory_results.flags(xapian.QueryParser.FLAG_PHRASE\
                        | xapian.QueryParser.FLAG_BOOLEAN\
                        | xapian.QueryParser.FLAG_LOVEHATE
                        | xapian.QueryParser.FLAG_WILDCARD
                        )
    else:
        form = SearchForm()

    
    return render_to_response(
      'search.html', 
      {
          'form' : form,
          'green_results' : green_results,
          'coalition_results' : coalition_results,
          'coalition_final_results' : coalition_final_results,
          'libdem_results' : libdem_results,
          'labour_results' : labour_results,
          'tory_results' : tory_results,
          
      },
      context_instance=RequestContext(request)
    )  
