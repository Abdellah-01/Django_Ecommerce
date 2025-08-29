from django.db import models
from abdellah_collections.models import Collection

# Create your models here.
class ImageBanner(models.Model):
    title = models.CharField(max_length=150)
    desktop_image = models.ImageField(upload_to='images/banners/desktop/')
    mobile_image = models.ImageField(upload_to='images/banners/mobile/')
    link = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True, help_text=("Leave Blank to All Products"))

    def __str__(self):
        return self.title
    
class FAQ(models.Model):
    HEADING_CHOICES = [
        ("orders_shipping", "orders & shipping"),
        ("payment", "payment"),
        ("returns", "returns & exchanges"),
        ("size_fit", "size & fit"),
        ("products", "products & materials"),
        ("offers", "offers & discounts"),
        ("account", "my account"),
        ("care", "care instructions"),
        ("store_policy", "store policies"),
    ]

    heading = models.CharField(max_length=100, choices=HEADING_CHOICES)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Order for display")

    class Meta:
        ordering = ["heading", "order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return f"{self.heading} - {self.question}"
    
class Enquiry(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"