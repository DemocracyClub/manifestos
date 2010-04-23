from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

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


def search(request):
    results = None
    libdem_results = labour_results = tory_results = None
    if request.POST:
        q = request.POST.get('q')
        indexer = Element.indexer
        libdem_results = indexer.search("%s party:libdem" % q)
        labour_results = indexer.search("%s party:labour" % q)
        tory_results = indexer.search("%s party:tory" % q)

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
    form = SearchForm(request.POST)

    
    return render_to_response(
      'search.html', 
      {
          'form' : form,
          'libdem_results' : libdem_results,
          'labour_results' : labour_results,
          'tory_results' : tory_results,
          
      },
      context_instance=RequestContext(request)
    )  
