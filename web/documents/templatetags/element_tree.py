from django.template import Library, Node
from django.template import Context, Variable
from misc import countryCodes
register = Library()

class ElementTree(Node):
    def __init__(self, code, varname):
        self.code = code            
        self.varname = varname
    
    def render(self, context):
        self.code = Variable(self.code).resolve(context)
        if self.code == "UK":
            self.code = "GB"
        
        context[self.varname] = countryCodes.country_codes(self.code)['name']
        return ''

@register.tag
def code_to_name(parser, token):
    bits = token.contents.split()
    return CodeToName(bits[1], bits[3])
