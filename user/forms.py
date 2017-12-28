from django import forms
from allauth.account.forms import LoginForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div, Submit

from django.shortcuts import reverse


class LoginForm(LoginForm):

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_action = reverse('account_login')
		self.helper.layout = Layout(
			Field('login', autocomplete='username'),
			Field('password', autocomplete='current-password'),
			HTML('<a class="float-right" href="{% url "account_reset_password" %}">忘记密码</a>'),
			Field('remember'),
			HTML('{% if redirect_field_value %}<input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}" />{% endif %}'),
			Div(
				Submit('signin', '登录', css_class="btn-primary col-8"),
				HTML('<a class="btn btn-outline-secondary col-4" href="{{ signup_url }}">注册</a>'),
				css_class='btn-group btn-block'
			),
		)


class SignupForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_action = reverse('account_signup')
		self.helper.layout = Layout(
			Field('username', autocomplete='username'),
			Field('email', autocomplete='new-password'),
			Field('password1', autocomplete='new-password'),
			Field('password2', autocomplete='new-password'),
			HTML('{% if redirect_field_value %}<input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}" />{% endif %}'),
			Submit('submit', '注册', css_class="btn-primary btn-block")
		)

	def signup(self, request, user):
		pass
