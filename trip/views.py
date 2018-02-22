from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import TripSerializer
from .models import Trip


class TripViewSet(ModelViewSet):
	template_name = 'app.html'
	queryset = Trip.objects.all()
	serializer_class = TripSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		return self.queryset.filter(user=self.request.user).order_by('-record__departureDate')
