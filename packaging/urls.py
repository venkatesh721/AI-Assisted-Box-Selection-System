from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ProductViewSet, ShippingBoxViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")
router.register("boxes", ShippingBoxViewSet, basename="box")
router.register("orders", OrderViewSet, basename="order")

urlpatterns = router.urls
