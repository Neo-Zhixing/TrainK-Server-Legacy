from rest_framework.viewsets import ModelViewSet
from .serializers import TripSerializer
from .models import Trip


class TripViewSet(ModelViewSet):
	template_name = 'triplist.html'
	queryset = Trip.objects.all()
	serializer_class = TripSerializer
