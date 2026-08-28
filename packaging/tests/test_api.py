from rest_framework import status
from rest_framework.test import APITestCase
from packaging.models import Order, OrderItem, Product, ShippingBox


class ApiTests(APITestCase):
    def create_product(self, **overrides):
        values = {"name": "Book", "length": "2.000", "width": "2.000", "height": "1.000", "weight": "1.000"}
        values.update(overrides)
        return Product.objects.create(**values)

    def test_create_and_read_product(self):
        response = self.client.post("/api/products/", {"name": "Mug", "length": "2", "width": "2", "height": "3", "weight": "1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.get(f"/api/products/{response.data['id']}/").status_code, status.HTTP_200_OK)

    def test_create_and_read_box(self):
        response = self.client.post("/api/boxes/", {"name": "Small", "internal_length": "5", "internal_width": "5", "internal_height": "5", "max_weight": "3", "cost": "1.50"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.get(f"/api/boxes/{response.data['id']}/").status_code, status.HTTP_200_OK)

    def test_create_order_with_nested_items(self):
        product = self.create_product()
        response = self.client.post("/api/orders/", {"reference": "ORDER-1", "order_items": [{"product_id": product.id, "quantity": 2}]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["items"][0]["quantity"], 2)

    def test_invalid_payload_and_duplicate_product_return_400(self):
        self.assertEqual(self.client.post("/api/products/", {"name": "Bad", "length": 0, "width": 1, "height": 1, "weight": 1}, format="json").status_code, status.HTTP_400_BAD_REQUEST)
        product = self.create_product()
        response = self.client.post("/api/orders/", {"order_items": [{"product_id": product.id, "quantity": 1}, {"product_id": product.id, "quantity": 1}]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recommendation_endpoint_returns_best_box(self):
        product = self.create_product()
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=product, quantity=2)
        ShippingBox.objects.create(name="Costly", internal_length=5, internal_width=2, internal_height=2, max_weight=3, cost=5)
        expected = ShippingBox.objects.create(name="Best", internal_length=5, internal_width=2, internal_height=2, max_weight=3, cost=2)
        response = self.client.post(f"/api/orders/{order.id}/recommend-box/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["recommended_box"]["id"], expected.id)

    def test_recommendation_returns_422_when_nothing_fits(self):
        product = self.create_product(weight="10.000")
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=product, quantity=1)
        ShippingBox.objects.create(name="Too weak", internal_length=10, internal_width=10, internal_height=10, max_weight=5, cost=1)
        self.assertEqual(self.client.post(f"/api/orders/{order.id}/recommend-box/").status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_unknown_order_returns_404(self):
        self.assertEqual(self.client.post("/api/orders/999/recommend-box/").status_code, status.HTTP_404_NOT_FOUND)
