from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Min


class Collection(models.Model):
    title = models.CharField(max_length=200)   # no unique=True
    slug = models.SlugField(max_length=255, blank=True)  # no unique=True
    description = models.TextField(blank=True)
    collection_image = models.ImageField(upload_to='images/collections/', blank=True)

    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'

    def get_url(self):
        return reverse('abdellah_collections:products_by_collection_page', args=[self.slug])  # changed from 'collection_slug
        
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        # generate unique slug
        while Collection.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug
        super().save(*args, **kwargs)

    @property
    def starting_price(self):
        """Return the minimum product price in this collection"""
        from products.models import Product
        min_price = Product.objects.filter(collection=self, is_available=True).aggregate(Min('price'))['price__min']
        return min_price
