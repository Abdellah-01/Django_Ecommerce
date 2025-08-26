from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.text import slugify
from django.urls import reverse
from django.shortcuts import redirect
from .models import Product, SizeGuide


# Custom Filter for MultiSelectField (sizes)
class SizeFilter(admin.SimpleListFilter):
    title = 'Sizes'
    parameter_name = 'sizes'

    def lookups(self, request, model_admin):
        return Product.SIZE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(sizes__icontains=self.value())
        return queryset


@admin.register(SizeGuide)
class SizeGuideAdmin(admin.ModelAdmin):
    list_display = ("title", "preview_image", "table_preview")
    search_fields = ("title",)
    list_filter = ("title",)
    readonly_fields = ("table_preview",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "image"),
        }),
        ("Size Table Data (JSON)", {
            "fields": ("table_data", "table_preview"),
            "description": "You can copy-paste JSON structure here to manage rows and columns."
        }),
    )

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:5px;" />', obj.image.url)
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
            html += f"<th style='border:1px solid #ddd;padding:4px;'>{col}</th>"
        html += "</tr>"
        for row in rows:
            html += f"<tr><td style='border:1px solid #ddd;padding:4px;'>{row.get('name')}</td>"
            for val in row.get("values", []):
                html += f"<td style='border:1px solid #ddd;padding:4px;text-align:center'>{val}</td>"
            html += "</tr>"
        html += "</table>"
        return format_html(html)

    table_preview.short_description = "Table Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_name", "price", "compare_at_price", "stock",
        "is_available", "collection", "category", "thumbnail", "created_at"
    )
    list_editable = ("price", "compare_at_price", "stock", "is_available")
    search_fields = ("product_name", "description", "tags")
    list_filter = ("is_available", "collection", "category", "created_at", SizeFilter)
    autocomplete_fields = ("collection", "category", "size_guide")
    readonly_fields = ("slug", "thumbnail_preview", "created_at", "modified_at")

    fieldsets = (
        ("Product Info", {
            "fields": ("product_name", "slug", "description", "more_info", "tags"),
        }),
        ("Categorization", {
            "fields": ("collection", "category"),
        }),
        ("Pricing & Stock", {
            "fields": ("price", "compare_at_price", "stock", "is_available"),
        }),
        ("Images", {
            "fields": ("product_image", "thumbnail_preview"),
        }),
        ("Sizes & Size Guide", {
            "fields": ("sizes", "size_guide"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "modified_at"),
        }),
    )

    # ✅ Admin Action to duplicate selected products
    actions = ["duplicate_products"]

    def duplicate_products(self, request, queryset):
        for obj in queryset:
            obj.pk = None  # Reset primary key
            original_slug = obj.slug
            obj.slug = None  # Force slug regeneration
            obj.product_name = f"{obj.product_name} (Copy)"
            obj.save()
            self.message_user(request, f"Duplicated product: {original_slug} → {obj.slug}", messages.SUCCESS)
    duplicate_products.short_description = "Duplicate selected products"

    # ✅ Add a "Duplicate" button in change form
    def response_change(self, request, obj):
        if "_duplicate" in request.POST:
            obj.pk = None
            obj.slug = None
            obj.product_name = f"{obj.product_name} (Copy)"
            obj.save()
            self.message_user(request, f"Product duplicated successfully!", messages.SUCCESS)
            return redirect(
                reverse("admin:app_product_change", args=[obj.pk])
            )
        return super().response_change(request, obj)

    def render_change_form(self, request, context, *args, **kwargs):
        context["adminform"].form.buttons = True
        return super().render_change_form(request, context, *args, **kwargs)

    def thumbnail(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:5px;" />', obj.product_image.url)
        return "No Image"
    thumbnail.short_description = "Preview"

    def thumbnail_preview(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="150" style="border-radius:8px;" />', obj.product_image.url)
        return "No Image"
    thumbnail_preview.short_description = "Image Preview"
