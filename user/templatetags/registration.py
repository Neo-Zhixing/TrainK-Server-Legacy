from django import template
from ..views.session import loginView


register = template.Library()


@register.simple_tag(takes_context=True)
def login_context(context):
	loginView.request = context.request
	return loginView.get_context_data()
