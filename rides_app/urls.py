from rest_framework.routers import DefaultRouter
from .views import RideViewSet

router = DefaultRouter()
router.register('rides', RideViewSet)

urlpatterns = router.urls