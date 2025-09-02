from django.contrib import admin
from django.utils.html import format_html
from .models import ImageBanner, FAQ, Enquiry
from django.contrib import admin
from django import forms
from sortedm2m_filter_horizontal_widget.forms import SortedFilteredSelectMultiple
from .models import FeaturedCollection
from django.utils.html import format_html
from django.urls import reverse  # ✅ import reverse!


class FeaturedCollectionForm(forms.ModelForm):
    class Meta:
        model = FeaturedCollection
        fields = "__all__"
        widgets = {
            "products": SortedFilteredSelectMultiple(),
        }


@admin.register(FeaturedCollection)
class FeaturedCollectionAdmin(admin.ModelAdmin):
    form = FeaturedCollectionForm
    list_display = ("title", "view_all_link", "collection_order", "ordered_products")
    list_editable = ("collection_order",)
    search_fields = ("title", "view_all_link__name", "products__name")
    list_filter = ("view_all_link",)
    ordering = ("collection_order",)

    def ordered_products(self, obj):
        products = obj.products.all()
        display_count = 5
        html = ""

        for p in products[:display_count]:
            url = reverse(
                "admin:%s_%s_change" % (p._meta.app_label, p._meta.model_name),
                args=[p.id]
            )
            html += format_html(
                '<a href="{}" style="display:inline-block; margin:2px; padding:2px 6px; '
                'background:#f0f0f0; text-decoration:none; color:#333;">'
                '<img src="{}" style="height:20px; width:20px; object-fit:cover; '
                'vertical-align:middle; margin-right:4px;">{}'
                '</a>',
                url,
                p.product_image.url if p.product_image else "https://via.placeholder.com/20",
                p.product_name
            )

        remaining = len(products) - display_count
        if remaining > 0:
            html += format_html(
                '<span style="display:inline-block; margin:2px; padding:4px 8px; '
                'background:#fff; color:#000;">+{} More</span>', remaining
            )

        return format_html(html)

    ordered_products.short_description = "Featured Products"



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

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('name', 'email', 'created_at', 'short_message')
    
    # Fields that are clickable links
    list_display_links = ('name', 'email')
    
    # Add search functionality
    search_fields = ('name', 'email', 'message')
    
    # Filter by date created
    list_filter = ('created_at',)
    
    # Ordering in admin
    ordering = ('-created_at',)
    
    # Make created_at read-only
    readonly_fields = ('created_at',)
    
    # Pagination (optional)
    list_per_page = 20
    
    # Optional: show first 50 chars of message
    def short_message(self, obj):
        return obj.message[:50] + ('...' if len(obj.message) > 50 else '')
    short_message.short_description = 'Message Preview'