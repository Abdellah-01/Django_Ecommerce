from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from abdellah_collections.models import Collection
from category.models import Category
from multiselectfield import MultiSelectField

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
        """Convert inch values to cm on the fly."""
        cm_data = {"columns": self.table_data.get("columns", []), "rows": []}
        for row in self.table_data.get("rows", []):
            inch_values = row.get("values", [])
            cm_values = [round(val * 2.54, 2) for val in inch_values]
            cm_data["rows"].append({
                "name": row.get("name"),
                "values": cm_values
            })
        return cm_data

    def __str__(self):
        return self.title

class Product(models.Model):
    SIZE_CHOICES = [
        ('xs', 'xs'),
        ('s', 's'),
        ('m', 'm'),
        ('l', 'l'),
        ('xl', 'xl'),
        ('xxl', 'xxl'),
        ('xxxl', 'xxxl'),
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
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # make slug unique & allow blank
    description = models.TextField(blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    product_image = models.ImageField(upload_to='images/products/')
    more_info = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    is_available = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    sizes = MultiSelectField(choices=SIZE_CHOICES, blank=True)
    size_guide = models.ForeignKey(SizeGuide, on_delete=models.SET_NULL, null=True, blank=True)

    def get_url(self):
        return reverse("products:product_details_page", args=[self.slug])


    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate if slug is empty
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
