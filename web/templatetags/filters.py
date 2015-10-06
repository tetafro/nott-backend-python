# Template decorators

from django import template

register = template.Library()


# Previous list item
@register.filter
def previous(iterable, current_index):
    try:
        return iterable[int(current_index)-1]
    except:
        return ''


# Next list item
@register.filter
def next(iterable, current_index):
    try:
        return iterable[int(current_index)+1]
    except:
        return ''
