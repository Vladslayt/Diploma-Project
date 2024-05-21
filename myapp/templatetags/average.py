# templatetags/average.py

from django import template

from django.db.models import Avg

register = template.Library()


@register.filter
def average(queryset, field_name):
    if queryset.exists():
        return queryset.aggregate(Avg(field_name)).get(f'{field_name}__avg')
    return 'N/A'
