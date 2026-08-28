from django.contrib import admin
from .models import Order, OrderItem, Product, ShippingBox


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "length", "width", "height", "weight")


@admin.register(ShippingBox)
class ShippingBoxAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "internal_length", "internal_width", "internal_height", "max_weight", "cost")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "reference", "created_at")
    inlines = [OrderItemInline]
