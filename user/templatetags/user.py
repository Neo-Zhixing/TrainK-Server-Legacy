import hashlib
from django import template
register = template.Library()


@register.filter
def hash(value):
	return hashlib.md5(value.lower().encode()).hexdigest()
