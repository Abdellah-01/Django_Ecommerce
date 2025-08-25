from django.contrib import admin
from .models import Cart, CartItem
from django.utils.html import format_html


class CartItemInline(admin.TabularInline):
    """Inline CartItems inside Cart admin"""
    model = CartItem
    extra = 1
    readonly_fields = ("sub_total",)
    fields = ("product", "size", "quantity", "is_active", "sub_total")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "date_added", "cart_items_count", "total_price")
    search_fields = ("cart_id",)
    list_filter = ("date_added",)
    date_hierarchy = "date_added"
    inlines = [CartItemInline]

    def cart_items_count(self, obj):
        return obj.cartitem_set.count()
    cart_items_count.short_description = "Items in Cart"

    def total_price(self, obj):
        return sum(item.sub_total for item in obj.cartitem_set.all())
    total_price.short_description = "Total Price"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("product_name", "cart", "quantity", "size", "colored_status", "sub_total")
    list_filter = ("is_active", "size", "cart__date_added")
    search_fields = ("product__product_name", "cart__cart_id")
    ordering = ("-id",)
    readonly_fields = ("sub_total",)

    actions = ["mark_active", "mark_inactive"]

    def product_name(self, obj):
        return obj.product.product_name
    product_name.admin_order_field = "product__product_name"
    product_name.short_description = "Product"

    def colored_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">● Active</span>')
        return format_html('<span style="color: red; font-weight: bold;">● Inactive</span>')
    colored_status.short_description = "Status"

    # Custom actions
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = "Mark selected items as Active"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Mark selected items as Inactive"
