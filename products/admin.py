from django.contrib import admin
from .models import Product, SizeGuide

@admin.register(SizeGuide)
class SizeGuideAdmin(admin.ModelAdmin):
    list_display = ("title",)   # shows title in list view
    search_fields = ("title",)  # makes it searchable

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'collection', 'category', 'price', 'stock', 'is_available', 'created_at', 'modified_at')
    search_fields = ('product_name', 'description', 'tags')
    list_filter = ('is_available', 'created_at', 'modified_at', 'collection', 'category')
    readonly_fields = ('slug',)  # Make slug read-only so it's not editable

admin.site.register(Product, ProductAdmin)
