from django.contrib import admin
from models import Element, Document
from treebeard.admin import TreeAdmin

class ElementAdmin(TreeAdmin):
    # prepopulated_fields = {"slug": ("name",)}
    pass

admin.site.register(Element, ElementAdmin)
admin.site.register(Document)