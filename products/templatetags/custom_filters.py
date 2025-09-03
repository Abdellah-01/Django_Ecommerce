from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Safely get dict item in Django template"""
    if dictionary and key in dictionary:
        return dictionary.get(key)
    return 0
