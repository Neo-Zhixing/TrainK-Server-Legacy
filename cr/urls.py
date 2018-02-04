from django.urls import path
from . import views

urlpatterns = [
	path('ticket/', views.TicketView.as_view()),
	path('ticket/order/', views.OrderView.as_view()),
	path('user/', views.UserView.as_view()),
	path('user/session/captcha', views.CaptchaView),
	path('user/session/', views.SessionView.as_view())
]
