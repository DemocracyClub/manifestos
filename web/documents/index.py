from djapian import space, Indexer, CompositeIndexer

from models import Element

# space.add_index(Element, attach_as='indexer')

class ElementIndexer(Indexer):
    fields = ['content', 'tags']
    tags = [
        ('document', 'document'),
        ('party', 'document.party'),
        ('tags', 'tags', 50),
    ]

space.add_index(Element, ElementIndexer, attach_as='indexer')

