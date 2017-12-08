from django.utils.dateparse import parse_duration
from django.utils.duration import _get_duration_components as durationComponents

from django import template
register = template.Library()


@register.filter(name='timedelta')
def Timedelta(value):
	duration = parse_duration(value)
	days, hours, minutes, seconds, miliseconds = durationComponents(duration)
	return '{:02d}:{:02d}'.format(hours, minutes)


@register.filter(name='connect')
def Connect(value):
	nameStr = ''
	for name in value:
		nameStr += name + '/'
	return nameStr[:-1]
