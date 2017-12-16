from datetime import timedelta
from django.utils.dateparse import parse_duration
from django.utils.duration import _get_duration_components as durationComponents

from django import template
register = template.Library()


@register.filter(name='timedelta')
def Timedelta(value):
	return parse_duration(value)


@register.filter(name='timedeltaStr')
def timedeltaStr(value):
	duration = parse_duration(value)
	days, hours, minutes, seconds, miliseconds = durationComponents(duration)
	return '{:02d}:{:02d}'.format(hours, minutes)


@register.filter
def timedeltaSec(value):
	duration = parse_duration(value)

	flag = 1
	if duration < timedelta():
		flag = -1
		duration *= -1
	return duration.seconds * flag


@register.filter
def timedeltaMin(value):
	return round(abs(timedeltaSec(value)) / 60)


@register.filter
def timedeltaMinus(value1, value2):
	return parse_duration(value1) - parse_duration(value2)


@register.filter
def timedeltaComponent(value, key):
	keys = ['days', 'hours', 'minutes', 'seconds', 'miliseconds']
	values = {}
	components = durationComponents(value)
	for index, value in enumerate(components):
		values[keys[index]] = value
	return values[key]


@register.filter
def connect(value):
	nameStr = ''
	for name in value:
		nameStr += name + '/'
	return nameStr[:-1]


@register.filter
def combine(value):
	nameStr = ''
	for name in value:
		nameStr += name + '\n'
	return nameStr[:-1]
