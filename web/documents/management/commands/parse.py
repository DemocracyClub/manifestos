"""
Parse an HTML document in to the Document/element model

"""
import sys

import django
from django.conf import settings
from pyquery import PyQuery as pq
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from documents.models import Document, Element
import codecs

import BeautifulSoup

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--party', '-p', dest='party',
        help='Party name'),
    )
    
    def handle(self, **options):
        party = options.get('party')
        # Hard code the file path for now.
        f_path = "manifestos/2010/%s/html.html" % (settings.PROJECT_ROOT, party,)
        f = codecs.open(f_path, 'r', 'utf8')
        d = BeautifulSoup.BeautifulSoup(f.read())
        
        tree_nodes = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6',]
        tag_pos = 0 #Always start at the root node
        doc_title = d.find('title').string
        try:
            document = Document.objects.get(title=doc_title, party=party)
        except:
            document = Document(title=doc_title, party=party)
            document.save()

        # Parents list, with a single, root, element
        parents = []
        for el in d.body:
            try:
                content = el
                tag = el.name
                # continue
                if tag in tree_nodes:
                    # We're dealing with a parent

                    tag_pos = tree_nodes.index(tag)

                    # Workout if this tag is 'under' the parent and 
                    # if it's not, take that parent out of the list
                    if tag_pos >= tree_nodes.index(tag):
                        parent_len = len(parents)
                        while parent_len > tag_pos:
                            parents.pop()
                            parent_len = len(parents)
                    if len(parents)<=0:
                        parents.append(Element().add_root(
                            document=document, 
                            content=content.string,
                            tag = tag,
                            ))
                    else:
                        parents.append(parents[-1].add_child(
                            document=document, 
                            content=content.string,
                            tag = tag,
                            ))
                
                else:
                    # print content
                    parents[-1].add_child(
                        document=document, 
                        content=content,
                        tag = tag,
                        )
                    print document
            except Exception, e:
                # print e
                # print el
                pass
                