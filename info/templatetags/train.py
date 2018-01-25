from .. import models
from django.utils.dateparse import parse_duration
from django.utils.duration import _get_duration_components as durationComponents

from django import template
register = template.Library()


@register.filter(name='timedelta')
def timedeltaValue(value):
	return parse_duration(value)


@register.filter
def timedeltaComp(value, key):
	keys = ['days', 'hours', 'minutes', 'seconds', 'miliseconds']
	values = {}
	components = durationComponents(value)
	for index, value in enumerate(components):
		values[keys[index]] = value
	return values[key]


@register.filter
def timedeltaStr(value):
	if not value:
		return ''
	days, hours, minutes, seconds, miliseconds = durationComponents(value)
	return '{:02d}:{:02d}'.format(hours, minutes)


@register.filter
def station(value):
	return models.Station.objects.get(pk=value) if isinstance(value, int) else None


@register.filter(name='abs')
def num_abs(value):
	return abs(value)
