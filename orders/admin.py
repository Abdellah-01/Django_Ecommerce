from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('product', 'quantity', 'product_price', 'size', 'ordered', 'created_at', 'updated_at')
    can_delete = False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'payment_method', 'amount_paid', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('payment_id', 'user__email', 'user__first_name', 'user__last_name', 'status')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'user', 'first_name', 'last_name', 'email', 'mobile_number',
        'order_total', 'tax', 'platform_fee', 'status', 'is_ordered', 'created_at'
    )
    list_filter = ('status', 'is_ordered', 'created_at', 'updated_at')
    search_fields = ('order_number', 'user__email', 'user__first_name', 'user__last_name', 'mobile_number', 'email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderProductInline]

    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'status', 'is_ordered', 'ip')
        }),
        ('Customer Info', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'mobile_number', 'company_name')
        }),
        ('Address', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'pincode')
        }),
        ('Payment & Totals', {
            'fields': ('payment', 'order_total', 'tax', 'platform_fee')
        }),
        ('Extra Info', {
            'fields': ('order_note',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    ordering = ('-created_at',)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'product', 'size', 'quantity', 'product_price', 'ordered', 'created_at')
    list_filter = ('ordered', 'created_at', 'updated_at')
    search_fields = ('order__order_number', 'product__product_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
