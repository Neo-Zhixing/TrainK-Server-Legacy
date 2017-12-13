from datetime import timedelta
from django.utils.dateparse import parse_duration
from django.utils.duration import _get_duration_components as durationComponents

from django import template
register = template.Library()


@register.filter(name='timedelta')
def Timedelta(value):
	duration = parse_duration(value)
	days, hours, minutes, seconds, miliseconds = durationComponents(duration)
	return '{:02d}:{:02d}'.format(hours, minutes)


@register.filter(name='timedeltaSec')
def TimedeltaSec(value):
	duration = parse_duration(value)

	flag = 1
	if duration < timedelta():
		flag = -1
		duration *= -1
	return duration.seconds * flag


@register.filter
def timedeltaMin(value):
	return round(abs(TimedeltaSec(value)) / 60)


@register.filter(name='connect')
def Connect(value):
	nameStr = ''
	for name in value:
		nameStr += name + '/'
	return nameStr[:-1]
