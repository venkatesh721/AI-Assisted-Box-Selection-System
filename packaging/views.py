from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, Product, ShippingBox
from .serializers import OrderSerializer, ProductSerializer, ShippingBoxSerializer
from .services import EmptyOrderError, recommend_box


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer


class ShippingBoxViewSet(viewsets.ModelViewSet):
    queryset = ShippingBox.objects.all().order_by("id")
    serializer_class = ShippingBoxSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product").order_by("id")
    serializer_class = OrderSerializer
    http_method_names = ["get", "post", "head", "options"]

    @action(detail=True, methods=["post"], url_path="recommend-box")
    def recommend_box(self, request, pk=None):
        order = self.get_object()
        try:
            recommendation = recommend_box(order.items.all(), ShippingBox.objects.all())
        except EmptyOrderError:
            return Response({"detail": "An order must contain at least one item."}, status=status.HTTP_400_BAD_REQUEST)

        if recommendation is None:
            return Response(
                {"detail": "No available box can accommodate this order under the configured packing rules."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        box = recommendation.box
        return Response({
            "order_id": order.id,
            "recommended_box": {"id": box.id, "name": box.name, "cost": str(box.cost)},
            "reason": "Lowest-cost box that satisfies weight, volume, and documented single-row packing rules.",
            "total_weight": str(recommendation.total_weight),
            "total_product_volume": str(recommendation.total_product_volume),
            "box_volume": str(recommendation.box_volume),
            "unused_volume": str(recommendation.unused_volume),
            "packing_axis": recommendation.packing_axis,
        })
