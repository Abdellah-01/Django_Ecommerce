from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Min, Max


class Category(models.Model):
    title = models.CharField(max_length=200)   # no unique=True
    slug = models.SlugField(max_length=255, blank=True)  # no unique=True
    description = models.TextField(blank=True)
    category_image = models.ImageField(upload_to='images/categories/', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_url(self):
        return reverse('category_urls:products_by_category_page', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        # generate unique slug
        while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug
        super().save(*args, **kwargs)
    
    @property
    def starting_price(self):
        """Return the minimum product price in this collection"""
        from products.models import Product
        min_price = Product.objects.filter(category=self, is_available=True).aggregate(Min('price'))['price__min']
        return min_price

    @property
    def max_price(self):
        """Return the maximum product price in this collection"""
        from products.models import Product
        max_price = Product.objects.filter(category=self, is_available=True).aggregate(Max('price'))['price__max']
        return max_price
    
    @property
    def total_products(self):
        """Return the total number of available products in this category"""
        from products.models import Product
        return Product.objects.filter(category=self, is_available=True).count()
    
    @property
    def my_products(self):
        """
        Returns a list of the first three product names associated with this category.
        """
        from products.models import Product
        return list(
            Product.objects.filter(category=self, is_available=True)
            .order_by('id')[:2]
            .values_list('product_name', flat=True)
        )