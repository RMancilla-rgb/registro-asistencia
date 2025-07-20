from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Permite hacer {{ form.field|add_class:"mi-css" }} para añadir attrs.
    """
    return field.as_widget(attrs={'class': css_class})
