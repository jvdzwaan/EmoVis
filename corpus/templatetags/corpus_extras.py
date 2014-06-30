"""
"""
from django import template
register = template.Library()


@register.inclusion_tag('year_link.html')
def year_link(year):
    return {'year': year}
