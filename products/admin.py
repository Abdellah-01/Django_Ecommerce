from django import forms
from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect
from .models import Product, ReviewRating, SizeGuide


# -----------------------------
# Product Form (no JS)
# -----------------------------
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # size -> model field mapping
        size_map = {
            "xs": "stock_xs",
            "s": "stock_s",
            "m": "stock_m",
            "l": "stock_l",
            "xl": "stock_xl",
            "xxl": "stock_xxl",
            "xxxl": "stock_xxxl",
            "28": "stock_28",
            "30": "stock_30",
            "32": "stock_32",
            "34": "stock_34",
            "36": "stock_36",
            "38": "stock_38",
            "40": "stock_40",
            "42": "stock_42",
            "44": "stock_44",
        }

        # Hide all stock fields by default
        for field in size_map.values():
            self.fields[field].widget = forms.HiddenInput()

        # Only show stock fields for selected sizes
        selected_sizes = []
        if self.data:  # POST
            selected_sizes = self.data.getlist("sizes")
        elif self.instance and self.instance.pk:  # Editing existing
            selected_sizes = self.instance.sizes or []

        for size in selected_sizes:
            field = size_map.get(size)
            if field:
                self.fields[field].widget = forms.NumberInput(attrs={"min": "0"})


# -----------------------------
# SizeGuide Admin
# -----------------------------
@admin.register(SizeGuide)
class SizeGuideAdmin(admin.ModelAdmin):
    list_display = ("title", "preview_image", "table_preview")
    search_fields = ("title",)
    list_filter = ("title",)
    readonly_fields = ("table_preview",)

    fieldsets = (
        ("Basic Info", {"fields": ("title", "image")}),
        ("Size Table Data (JSON)", {
            "fields": ("table_data", "table_preview"),
            "description": "Enter JSON structure to manage rows and columns."
        }),
    )

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:5px;" />',
                obj.image.url
            )
        return "No Image"
    preview_image.short_description = "Image"

    def table_preview(self, obj):
        if not obj.table_data:
            return "No table data"
        columns = obj.table_data.get("columns", [])
        rows = obj.table_data.get("rows", [])
        html = "<table style='border-collapse:collapse; border:1px solid #ddd;'>"
        html += "<tr><th style='border:1px solid #ddd;padding:4px;'>Metric</th>"
        for col in columns:
            html += f"<th style='border:1px solid #ddd;padding:4px;text-align:center'>{col}</th>"
        html += "</tr>"
        for row in rows:
            html += f"<tr><td style='border:1px solid #ddd;padding:4px;'>{row.get('name')}</td>"
            for val in row.get("values", []):
                html += f"<td style='border:1px solid #ddd;padding:4px;text-align:center'>{val}</td>"
            html += "</tr>"
        html += "</table>"
        return format_html(html)
    table_preview.short_description = "Table Preview"


# -----------------------------
# Product Admin
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    list_display = (
        "product_name", "price", "compare_at_price", "total_stock",
        "is_available", "collection", "category", "thumbnail", "created_at"
    )
    list_editable = ("price", "compare_at_price", "is_available")
    search_fields = ("product_name", "description", "tags")
    list_filter = ("is_available", "collection", "category", "created_at")
    autocomplete_fields = ("collection", "category", "size_guide")
    readonly_fields = ("slug", "thumbnail_preview", "created_at", "modified_at")

    fieldsets = (
        ("Product Info", {"fields": ("product_name", "slug", "description", "more_info", "tags")}),
        ("Categorization", {"fields": ("collection", "category")}),
        ("Pricing & Availability", {"fields": ("price", "compare_at_price", "is_available")}),
        ("Sizes and Stocks", {
            "fields": (
                "sizes", "size_guide",
                "stock_xs","stock_s","stock_m","stock_l","stock_xl","stock_xxl","stock_xxxl",
                "stock_28","stock_30","stock_32","stock_34","stock_36","stock_38","stock_40","stock_42","stock_44"
            )
        }),
        ("Images", {"fields": ("product_image", "thumbnail_preview")}),
        ("Timestamps", {"fields": ("created_at", "modified_at")}),
    )

    # Thumbnail for list view
    def thumbnail(self, obj):
        if obj.product_image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:5px;" />',
                obj.product_image.url
            )
        return "No Image"
    thumbnail.short_description = "Preview"

    def thumbnail_preview(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="150" style="border-radius:8px;" />', obj.product_image.url)
        return "No Image"
    thumbnail_preview.short_description = "Image Preview"

    def total_stock(self, obj):
        fields = [
            "stock_xs","stock_s","stock_m","stock_l","stock_xl","stock_xxl","stock_xxxl",
            "stock_28","stock_30","stock_32","stock_34","stock_36","stock_38","stock_40","stock_42","stock_44"
        ]
        return sum(getattr(obj, f, 0) for f in fields)
    total_stock.short_description = "Stock"

    # Duplicate product action
    actions = ["duplicate_products"]

    def duplicate_products(self, request, queryset):
        for obj in queryset:
            obj.pk = None
            obj.slug = None
            obj.product_name = f"{obj.product_name} (Copy)"
            obj.save()
            self.message_user(request, f"Duplicated product: {obj.product_name}", messages.SUCCESS)
    duplicate_products.short_description = "Duplicate selected products"

    def response_change(self, request, obj):
        if "_duplicate" in request.POST:
            obj.pk = None
            obj.slug = None
            obj.product_name = f"{obj.product_name} (Copy)"
            obj.save()
            self.message_user(request, "Product duplicated successfully!", messages.SUCCESS)
            return redirect(reverse("admin:products_product_change", args=[obj.pk]))
        return super().response_change(request, obj)


admin.site.register(ReviewRating)