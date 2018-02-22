from django.urls import path, re_path
from rest_framework import routers
from allauth.account import views as allauth_views
from . import views

urlpatterns = [
	path('', views.UserView.as_view(), name='account_signup'),
	path('session/', views.SessionView.as_view(), name='account_login'),
	path('email/key:<key>/', allauth_views.ConfirmEmailView.as_view(template_name='email/confirm.html'), name='account_confirm_email'),

	path('password/', views.PasswordView.as_view(), name='account_reset_password'),
	path('password/', views.PasswordView.as_view(), name='account_change_password'),
	path('password/<uidb36>:<key>/', allauth_views.PasswordResetFromKeyView.as_view(template_name='password/confirm.html'), name='account_reset_password_from_key'),
	path('password/done/', allauth_views.password_reset_done, name='account_reset_password_done'),
	re_path('setting', views.SettingView.as_view(), name="account_settings"),
]

router = routers.DefaultRouter()
router.register('email', views.EmailViewSet, base_name='email')
urlpatterns += router.urls
