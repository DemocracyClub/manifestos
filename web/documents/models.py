from django.db import models
from django.contrib.contenttypes import generic

from django.db import models

from taggit.managers import TaggableManager

from treebeard.mp_tree import MP_Node



from promises.models import Promise

class Document(models.Model):
    title = models.CharField(blank=True, max_length=255)
    party = models.CharField(blank=True, max_length=100)
    def __unicode__(self):
        return self.title


class Element(MP_Node):
    document = models.ForeignKey(Document)
    content = models.TextField(blank=True)
    tag = models.CharField(blank=True, max_length=20)
    promise = generic.GenericRelation(Promise)
    
    tags = TaggableManager()
    
    def __unicode__(self):
        return "element"
