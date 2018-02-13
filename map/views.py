from rest_framework.views import APIView
from rest_framework.response import Response


class AbstructMapView(APIView):
	template_name = 'abstruct.html'

	def get(self, request):
		return Response({})
