from decimal import Decimal
from django.test import TestCase
from packaging.models import Order, OrderItem, Product, ShippingBox
from packaging.services import EmptyOrderError, recommend_box, unique_orientations


class SelectionServiceTests(TestCase):
    def product(self, name="Product", dimensions=(1, 1, 1), weight=1):
        return Product.objects.create(name=name, length=dimensions[0], width=dimensions[1], height=dimensions[2], weight=weight)

    def box(self, name="Box", dimensions=(10, 10, 10), max_weight=10, cost=1):
        return ShippingBox.objects.create(name=name, internal_length=dimensions[0], internal_width=dimensions[1], internal_height=dimensions[2], max_weight=max_weight, cost=cost)

    def order_with(self, product, quantity=1):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=product, quantity=quantity)
        return order

    def recommend(self, order, boxes):
        return recommend_box(order.items.select_related("product"), boxes)

    def test_unique_orientations_deduplicates_repeated_dimensions(self):
        product = self.product(dimensions=(2, 2, 3))
        self.assertEqual(len(unique_orientations(product)), 3)

    def test_single_product_fits_without_rotation(self):
        order = self.order_with(self.product(dimensions=(4, 3, 2)))
        box = self.box(dimensions=(5, 4, 3))
        self.assertEqual(self.recommend(order, [box]).box, box)

    def test_product_can_fit_only_after_rotation(self):
        order = self.order_with(self.product(dimensions=(2, 3, 4)))
        box = self.box(dimensions=(4, 2, 3))
        self.assertEqual(self.recommend(order, [box]).box, box)

    def test_product_that_cannot_fit_any_orientation_is_rejected(self):
        order = self.order_with(self.product(dimensions=(5, 5, 5)))
        self.assertIsNone(self.recommend(order, [self.box(dimensions=(4, 4, 4))]))

    def test_weight_equal_to_capacity_is_accepted(self):
        order = self.order_with(self.product(weight=5))
        box = self.box(max_weight=5)
        self.assertEqual(self.recommend(order, [box]).box, box)

    def test_weight_over_capacity_is_rejected(self):
        order = self.order_with(self.product(weight=Decimal("5.001")))
        self.assertIsNone(self.recommend(order, [self.box(max_weight=5)]))

    def test_volume_over_box_volume_is_rejected(self):
        order = self.order_with(self.product(dimensions=(3, 3, 3)))
        self.assertIsNone(self.recommend(order, [self.box(dimensions=(2, 2, 2))]))

    def test_multiple_products_fit_in_single_row(self):
        order = self.order_with(self.product(dimensions=(3, 2, 2)), quantity=2)
        box = self.box(dimensions=(6, 2, 2))
        self.assertEqual(self.recommend(order, [box]).box, box)

    def test_multiple_products_exceed_single_row_length(self):
        order = self.order_with(self.product(dimensions=(3, 2, 2)), quantity=3)
        box = self.box(dimensions=(8, 2, 2))
        self.assertIsNone(self.recommend(order, [box]))

    def test_unit_that_cannot_fit_cross_section_rejects_box(self):
        order = self.order_with(self.product(dimensions=(10, 3, 3)))
        self.assertIsNone(self.recommend(order, [self.box(dimensions=(10, 2, 2))]))

    def test_lowest_cost_box_wins(self):
        order = self.order_with(self.product())
        expensive = self.box(name="Expensive", cost=5)
        cheap = self.box(name="Cheap", cost=2)
        self.assertEqual(self.recommend(order, [expensive, cheap]).box, cheap)

    def test_equal_cost_uses_lower_unused_volume(self):
        order = self.order_with(self.product(dimensions=(2, 2, 2)))
        large = self.box(name="Large", dimensions=(5, 5, 5), cost=2)
        small = self.box(name="Small", dimensions=(3, 3, 3), cost=2)
        self.assertEqual(self.recommend(order, [large, small]).box, small)

    def test_equal_candidates_fall_back_to_id(self):
        order = self.order_with(self.product())
        first = self.box(name="First", cost=2)
        second = self.box(name="Second", cost=2)
        self.assertEqual(self.recommend(order, [second, first]).box, first)

    def test_empty_order_raises_clear_error(self):
        with self.assertRaises(EmptyOrderError):
            recommend_box([], [self.box()])

    def test_no_suitable_box_returns_none(self):
        order = self.order_with(self.product(weight=10))
        self.assertIsNone(self.recommend(order, [self.box(max_weight=9)]))
