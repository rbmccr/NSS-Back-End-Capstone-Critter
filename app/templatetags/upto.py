from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

# this is used to split a {{ var|timesince }} string at the delimiter (e.g. comma)

@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]
upto.is_safe = True