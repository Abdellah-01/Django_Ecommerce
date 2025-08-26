from django.contrib import admin
from django.utils.html import format_html
from .models import ImageBanner, FAQ


@admin.register(ImageBanner)
class ImageBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "desktop_preview", "mobile_preview", "link")
    search_fields = ("title",)
    list_filter = ("link",)
    ordering = ("title",)
    
    readonly_fields = ("desktop_preview", "mobile_preview")

    fieldsets = (
        ("Banner Info", {
            "fields": ("title", "link")
        }),
        ("Images", {
            "fields": ("desktop_image", "desktop_preview", "mobile_image", "mobile_preview"),
            "classes": ("collapse",),
        }),
    )

    def desktop_preview(self, obj):
        if obj.desktop_image:
            return format_html('<img src="{}" width="200" style="border-radius:8px;"/>', obj.desktop_image.url)
        return "No Image"
    desktop_preview.short_description = "Desktop Preview"

    def mobile_preview(self, obj):
        if obj.mobile_image:
            return format_html('<img src="{}" width="120" style="border-radius:8px;"/>', obj.mobile_image.url)
        return "No Image"
    mobile_preview.short_description = "Mobile Preview"


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("heading", "question", "order", "short_answer")
    list_filter = ("heading",)
    search_fields = ("question", "answer")
    ordering = ("heading", "order")

    # Make "order" editable directly in list view
    list_editable = ("order",)

    fieldsets = (
        ("FAQ Details", {
            "fields": ("heading", "question", "answer")
        }),
        ("Display Options", {
            "fields": ("order",),
            "classes": ("collapse",),
        }),
    )

    def short_answer(self, obj):
        return obj.answer[:70] + "..." if len(obj.answer) > 70 else obj.answer
    short_answer.short_description = "Answer Preview"
