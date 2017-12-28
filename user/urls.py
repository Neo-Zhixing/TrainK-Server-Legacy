from django.views.generic import TemplateView
from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.UserView.as_view(), name='account_signup'),
	path('session/', views.SessionView.as_view(), name='account_login'),
	path('email/<str:key>', views.EmailView.as_view(), name='account_confirm_email'),
	path('password/', views.PasswordView.as_view(), name='account_reset_password'),
	re_path('setting/', TemplateView.as_view(template_name='settings.html'), name="account_settings"),
]
