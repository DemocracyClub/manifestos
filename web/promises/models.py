from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Promise(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(blank=False, null=False, max_length=100)
    content_object = generic.GenericForeignKey('content_type', 'object_id')


    def __unicode__(self):
        return "%s" % self.content_object

