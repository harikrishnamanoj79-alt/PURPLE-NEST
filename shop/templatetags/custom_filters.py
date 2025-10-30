from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply two numeric values in a Django template."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
