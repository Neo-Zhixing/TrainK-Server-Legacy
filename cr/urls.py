from django.urls import path
from . import views

urlpatterns = [
	path('ticket/', views.TicketListView),
	path('user/session/', views.LoginView.as_view())
]
