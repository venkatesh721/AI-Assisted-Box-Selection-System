from rest_framework import serializers
from .models import Order, OrderItem, Product, ShippingBox


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "length", "width", "height", "weight")


class ShippingBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingBox
        fields = ("id", "name", "internal_length", "internal_width", "internal_height", "max_weight", "cost")


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product")
    quantity = serializers.IntegerField(min_value=1)


class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)
    order_items = OrderItemInputSerializer(many=True, write_only=True, required=True)

    class Meta:
        model = Order
        fields = ("id", "reference", "created_at", "items", "order_items")
        read_only_fields = ("id", "created_at", "items")

    def validate_order_items(self, items):
        if not items:
            raise serializers.ValidationError("An order must contain at least one item.")
        product_ids = [item["product"].id for item in items]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("A product may appear only once in an order.")
        return items

    def create(self, validated_data):
        items = validated_data.pop("order_items")
        order = Order.objects.create(**validated_data)
        OrderItem.objects.bulk_create([
            OrderItem(order=order, product=item["product"], quantity=item["quantity"])
            for item in items
        ])
        return order
