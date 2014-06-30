"""
"""
from django import template
register = template.Library()


@register.inclusion_tag('year_link.html')
def year_link(year):
    return {'year': year}


@register.inclusion_tag('title_link.html')
def title_link(title):
    return {
        'ti_id': title.ti_id,
        'title': title.titel
    }
