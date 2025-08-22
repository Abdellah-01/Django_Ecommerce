from django.db import models
from django.utils.text import slugify

class Collection(models.Model):
    title = models.CharField(max_length=200)   # no unique=True
    slug = models.SlugField(max_length=255, blank=True)  # no unique=True
    description = models.TextField(blank=True)
    collection_image = models.ImageField(upload_to='images/collections/', blank=True)

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
