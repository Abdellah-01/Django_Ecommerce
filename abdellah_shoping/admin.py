from django.contrib import admin
from django.utils.html import format_html
from .models import ImageBanner

@admin.register(ImageBanner)
class ImageBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "desktop_preview", "mobile_preview", "linked_collection", "link")
    search_fields = ("title", "link__title")
    list_filter = ("link",)
    ordering = ("-id",)
    list_editable = ("link",)  # Inline edit for link field
    list_per_page = 20

    # Show desktop image preview
    def desktop_preview(self, obj):
        if obj.desktop_image:
            return format_html('<img src="{}" style="height:50px; border-radius:5px;" />', obj.desktop_image.url)
        return "No Image"
    desktop_preview.short_description = "Desktop Image"

    # Show mobile image preview
    def mobile_preview(self, obj):
        if obj.mobile_image:
            return format_html('<img src="{}" style="height:50px; border-radius:5px;" />', obj.mobile_image.url)
        return "No Image"
    mobile_preview.short_description = "Mobile Image"

    # Clickable collection link
    def linked_collection(self, obj):
        if obj.link:
            return format_html('<a href="/admin/abdellah_collections/collection/{}/change/">{}</a>', obj.link.id, obj.link.title)
        return "No Collection"
    linked_collection.short_description = "Linked Collection"
