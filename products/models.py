from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from flask import json
from abdellah_collections.models import Collection
from accounts.models import Account
from category.models import Category
from multiselectfield import MultiSelectField
from decimal import Decimal, ROUND_HALF_UP
from ckeditor.fields import RichTextField
from django.db.models import Avg, Count


class SizeGuide(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/size_guides/", blank=True, null=True)

    table_data = models.JSONField(
        default=dict,
        help_text=(
            'Enter JSON in the format:<br>'
            '{<br>'
            '  "columns": ["XS", "S", "M", "L", "XL", "XXL"],<br>'
            '  "rows": [<br>'
            '    {"name": "Bust", "values": [34, 36, 38, 40, 42, 44]},<br>'
            '    {"name": "Waist", "values": [26, 28, 30, 32, 34, 36]},<br>'
            '    {"name": "Hips", "values": [36, 38, 40, 42, 44, 46]}<br>'
            '  ]<br>'
            '}'
        )
    )

    def get_cm_table(self):
        """Convert inch values to cm on the fly (rounded half up)."""
        cm_data = {"columns": self.table_data.get("columns", []), "rows": []}
        for row in self.table_data.get("rows", []):
            inch_values = row.get("values", [])
            cm_values = [int(Decimal(val * 2.54).quantize(0, ROUND_HALF_UP)) for val in inch_values]
            cm_data["rows"].append({
                "name": row.get("name"),
                "values": cm_values
            })
        return cm_data

    def __str__(self):
        return self.title

class Product(models.Model):
    SIZE_CHOICES = [
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
        ('28', '28'),
        ('30', '30'),
        ('32', '32'),
        ('34', '34'),
        ('36', '36'),
        ('38', '38'),
        ('40', '40'),
        ('42', '42'),
        ('44', '44'),
    ]
    
    product_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = RichTextField(blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='images/products/')
    more_info = RichTextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    sizes = MultiSelectField(choices=SIZE_CHOICES, blank=True)
    size_guide = models.ForeignKey(SizeGuide, on_delete=models.SET_NULL, null=True, blank=True)


    # Stock per size
    stock_xs = models.PositiveIntegerField(default=0)
    stock_s = models.PositiveIntegerField(default=0)
    stock_m = models.PositiveIntegerField(default=0)
    stock_l = models.PositiveIntegerField(default=0)
    stock_xl = models.PositiveIntegerField(default=0)
    stock_xxl = models.PositiveIntegerField(default=0)
    stock_xxxl = models.PositiveIntegerField(default=0)
    stock_28 = models.PositiveIntegerField(default=0)
    stock_30 = models.PositiveIntegerField(default=0)
    stock_32 = models.PositiveIntegerField(default=0)
    stock_34 = models.PositiveIntegerField(default=0)
    stock_36 = models.PositiveIntegerField(default=0)
    stock_38 = models.PositiveIntegerField(default=0)
    stock_40 = models.PositiveIntegerField(default=0)
    stock_42 = models.PositiveIntegerField(default=0)
    stock_44 = models.PositiveIntegerField(default=0)

    def get_url(self):
        return reverse("products:product_details_page", args=[self.slug])
    
    @property
    def savings(self):
        if self.compare_at_price and self.price:
            return max(self.compare_at_price - self.price, 0)
        return 0

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.product_name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name
    
    @property
    def total_stock(self):
        """Return the sum of all size-specific stock fields."""
        size_fields = [
            "stock_xs", "stock_s", "stock_m", "stock_l", "stock_xl",
            "stock_xxl", "stock_xxxl", "stock_28", "stock_30", "stock_32",
            "stock_34", "stock_36", "stock_38", "stock_40", "stock_42", "stock_44",
        ]
        return sum(getattr(self, field, 0) for field in size_fields)

    
    def stock_for_size(self, size):
        """Return stock for a given size (case-insensitive)."""
        return getattr(self, f"stock_{str(size).lower()}", 0)

    def get_stock_for(self, size):
        """Safe wrapper for templates (avoids template limitations)."""
        return self.stock_for_size(size)
    
    def size_stock_dict(self):
        """Return dictionary of size -> stock"""
        return {size: self.stock_for_size(size) for size in self.sizes}

    @property
    def size_stock_json(self):
        """Return JSON string for templates"""
        return json.dumps(self.size_stock_dict())
    
    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    @property
    def count_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

