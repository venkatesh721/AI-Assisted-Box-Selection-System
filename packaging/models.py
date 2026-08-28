from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models


POSITIVE_DECIMAL = MinValueValidator(Decimal("0.001"))
NON_NEGATIVE_DECIMAL = MinValueValidator(Decimal("0"))


class Product(models.Model):
    name = models.CharField(max_length=200)
    length = models.DecimalField(max_digits=10, decimal_places=3, validators=[POSITIVE_DECIMAL])
    width = models.DecimalField(max_digits=10, decimal_places=3, validators=[POSITIVE_DECIMAL])
    height = models.DecimalField(max_digits=10, decimal_places=3, validators=[POSITIVE_DECIMAL])
    weight = models.DecimalField(max_digits=10, decimal_places=3, validators=[POSITIVE_DECIMAL])

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(length__gt=0), name="product_length_positive"),
            models.CheckConstraint(condition=models.Q(width__gt=0), name="product_width_positive"),
            models.CheckConstraint(condition=models.Q(height__gt=0), name="product_height_positive"),
            models.CheckConstraint(condition=models.Q(weight__gt=0), name="product_weight_positive"),
        ]

    def __str__(self):
        return self.name


class ShippingBox(models.Model):
    name = models.CharField(max_length=200)
    internal_length = models.DecimalField(max_digits=10, decimal_places=3, validators=[POSITIVE_DECIMAL])
    internal_width = models.DecimalField(max_digits=10, decimal_places=3, validators=[POSITIVE_DECIMAL])
    internal_height = models.DecimalField(max_digits=10, decimal_places=3, validators=[POSITIVE_DECIMAL])
    max_weight = models.DecimalField(max_digits=10, decimal_places=3, validators=[POSITIVE_DECIMAL])
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[NON_NEGATIVE_DECIMAL])

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(internal_length__gt=0), name="box_length_positive"),
            models.CheckConstraint(condition=models.Q(internal_width__gt=0), name="box_width_positive"),
            models.CheckConstraint(condition=models.Q(internal_height__gt=0), name="box_height_positive"),
            models.CheckConstraint(condition=models.Q(max_weight__gt=0), name="box_weight_positive"),
            models.CheckConstraint(condition=models.Q(cost__gte=0), name="box_cost_non_negative"),
        ]

    def __str__(self):
        return self.name


class Order(models.Model):
    reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference or f"Order {self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(quantity__gte=1), name="order_item_quantity_positive")]

    def __str__(self):
        return f"{self.quantity} x {self.product}"
