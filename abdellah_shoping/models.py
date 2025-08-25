from django.db import models
from abdellah_collections.models import Collection

# Create your models here.
class ImageBanner(models.Model):
    title = models.CharField(max_length=150)
    desktop_image = models.ImageField(upload_to='images/banners/desktop/')
    mobile_image = models.ImageField(upload_to='images/banners/mobile/')
    link = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title