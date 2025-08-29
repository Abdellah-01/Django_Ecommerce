from django.db import models
from products.models import Product
from accounts.models import Account
from decimal import Decimal
from bson.decimal128 import Decimal128

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Product, blank=True, related_name="variation_items")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    size = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def to_decimal(self, value):
        """Convert Decimal128 or other numeric values to Python Decimal."""
        if isinstance(value, Decimal128):
            return value.to_decimal()
        return Decimal(str(value))
    
    @property
    def sub_total(self):
        qty = self.quantity or 0
        return self.to_decimal(self.product.price) * qty

    def __unicode__(self):
        return f"{self.product.product_name} (x{self.quantity})"
