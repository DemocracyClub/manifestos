from django import forms
from taggit.forms import TagField
from models import Element

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100)


class TagForm(forms.ModelForm):
    tags = TagField()

    class Meta:
        model = Element
        fields = ('tags',)