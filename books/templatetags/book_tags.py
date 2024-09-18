from django import template
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured

register = template.Library()

@register.simple_tag
def admin_edit(obj):
    """
    Generate the URL for editing an object in the admin interface.
    """
    return reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.pk])
