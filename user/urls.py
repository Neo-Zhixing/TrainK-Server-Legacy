from django.views.generic import TemplateView
from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.UserView.as_view()),
	path('session/', views.SessionView.as_view()),
	path('password/', views.PasswordView.as_view()),
	re_path('setting/', TemplateView.as_view(template_name='settings.html')),
]
