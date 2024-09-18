from django import template
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured

register = template.Library()

@register.simple_tag
def admin_edit(obj):
    """
    Generate the URL for editing an object in the admin interface.
    """
    try:
        if not hasattr(obj, '_meta'):
            raise ImproperlyConfigured('Object is not a Django model instance.')
        return reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.pk])
    except Exception as e:
        return f'Error generating admin URL: {str(e)}'
