# Template decorators

from django import template

register = template.Library()


@register.filter
def prev_element(iterable, current_index):
    try:
        return iterable[int(current_index)-1]
    except:
        return ''


@register.filter
def next_element(iterable, current_index):
    try:
        return iterable[int(current_index)+1]
    except:
        return ''


@register.filter
def range_diff(number_1, number_2):
    return range(number_1 - number_2)


@register.filter
def is_folder(item):
    if item.__class__.__name__ == 'Folder':
        return True
    else:
        return False
