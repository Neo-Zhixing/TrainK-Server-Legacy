from rest_framework import routers
from . import views

urlpatterns = [
]

router = routers.DefaultRouter()
router.register('', views.TripViewSet)
urlpatterns += router.urls
