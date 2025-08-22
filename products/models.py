from django.db import models
from django.utils.text import slugify
from abdellah_collections.models import Collection
from category.models import Category

class Product(models.Model):
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
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

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
