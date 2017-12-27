from django.urls import path, re_path
from .views import session, user

urlpatterns = [
	path('', user.UserView.as_view()),
	path('session', session.SessionView.as_view()),
	re_path('', user.UserView.as_view()),
]
