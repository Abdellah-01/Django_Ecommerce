from django.db import models

# Create your models here.
class Collection(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    collection_image = models.ImageField(upload_to='images/collections/', blank=True)

    def __str__(self):
        return self.title