from django.contrib import admin
from django.utils.html import format_html
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "image_preview")
    list_display_links = ("title", "slug")
    search_fields = ("title", "slug", "description")
    list_filter = ("title",)
    readonly_fields = ("slug", "image_preview")  # slug auto-handled

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "slug", "description")
        }),
        ("Image", {
            "fields": ("category_image", "image_preview")
        }),
    )

    def image_preview(self, obj):
        if obj.category_image:
            return format_html(
                '<img src="{}" style="width: 50px; height:auto;" />',
                obj.category_image.url,
            )
        return "No Image"

    image_preview.short_description = "Preview"
