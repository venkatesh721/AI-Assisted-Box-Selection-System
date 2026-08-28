from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from packaging.models import Order, OrderItem, Product, ShippingBox


class ModelValidationTests(TestCase):
    def test_product_rejects_zero_or_negative_measurements(self):
        product = Product(name="Invalid", length=0, width=1, height=1, weight=-1)
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_box_rejects_invalid_measurements_and_cost(self):
        box = ShippingBox(name="Invalid", internal_length=1, internal_width=0, internal_height=1, max_weight=-1, cost=-1)
        with self.assertRaises(ValidationError):
            box.full_clean()

    def test_order_item_rejects_zero_quantity(self):
        product = Product.objects.create(name="Item", length=1, width=1, height=1, weight=1)
        item = OrderItem(order=Order.objects.create(), product=product, quantity=0)
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_decimal_values_are_preserved(self):
        product = Product.objects.create(name="Precise", length=Decimal("1.125"), width=1, height=1, weight=Decimal("0.250"))
        self.assertEqual(product.length, Decimal("1.125"))
