"""Deterministic, framework-light shipping-box selection logic."""
from dataclasses import dataclass
from decimal import Decimal
from itertools import permutations
from typing import Iterable


class EmptyOrderError(ValueError):
    """Raised when a recommendation is requested for an order with no units."""


@dataclass(frozen=True)
class Recommendation:
    box: object
    total_weight: Decimal
    total_product_volume: Decimal
    box_volume: Decimal
    unused_volume: Decimal
    packing_axis: str


def unique_orientations(product) -> tuple[tuple[Decimal, Decimal, Decimal], ...]:
    """Return all distinct (axis, cross-section-1, cross-section-2) orientations."""
    dimensions = (product.length, product.width, product.height)
    return tuple(dict.fromkeys(permutations(dimensions)))


def _box_axes(box):
    return (
        ("internal_length", box.internal_length, box.internal_width, box.internal_height),
        ("internal_width", box.internal_width, box.internal_length, box.internal_height),
        ("internal_height", box.internal_height, box.internal_length, box.internal_width),
    )


def _minimum_row_length(product, cross_one: Decimal, cross_two: Decimal):
    """Return the shortest valid row-axis dimension, or None if none fit."""
    valid_lengths = [
        row_length
        for row_length, product_cross_one, product_cross_two in unique_orientations(product)
        if product_cross_one <= cross_one and product_cross_two <= cross_two
    ]
    return min(valid_lengths) if valid_lengths else None


def recommend_box(order_items: Iterable, boxes: Iterable) -> Recommendation | None:
    """Choose the least-cost box that meets the documented single-row rule.

    ``order_items`` only needs ``product`` and ``quantity`` attributes; ``boxes``
    only needs the ShippingBox dimension, capacity, cost, and id attributes.
    """
    units = [item.product for item in order_items for _ in range(item.quantity)]
    if not units:
        raise EmptyOrderError("An order must contain at least one item.")

    total_weight = sum((product.weight for product in units), Decimal("0"))
    total_product_volume = sum(
        (product.length * product.width * product.height for product in units), Decimal("0")
    )
    candidates = []

    for box in boxes:
        if total_weight > box.max_weight:
            continue
        box_volume = box.internal_length * box.internal_width * box.internal_height
        if total_product_volume > box_volume:
            continue

        valid_axes = []
        for axis_name, axis_length, cross_one, cross_two in _box_axes(box):
            required_length = Decimal("0")
            for product in units:
                minimum_length = _minimum_row_length(product, cross_one, cross_two)
                if minimum_length is None:
                    break
                required_length += minimum_length
            else:
                if required_length <= axis_length:
                    valid_axes.append((required_length, axis_name))

        if valid_axes:
            # This choice does not change ranking; it makes the reported axis stable.
            _, packing_axis = min(valid_axes, key=lambda result: (result[0], result[1]))
            unused_volume = box_volume - total_product_volume
            candidates.append(
                Recommendation(box, total_weight, total_product_volume, box_volume, unused_volume, packing_axis)
            )

    if not candidates:
        return None
    return min(candidates, key=lambda result: (result.box.cost, result.unused_volume, result.box.id))
