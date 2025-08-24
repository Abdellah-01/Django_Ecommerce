from decimal import Decimal
from bson.decimal128 import Decimal128
from .models import Cart, CartItem
from .views import _cart_id


def cart_context(request):
    cart_items = []
    total = Decimal('0.00')
    quantity = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active__in=[True])

        for item in cart_items:
            # Convert price to Decimal if needed
            price = item.product.price
            if isinstance(price, Decimal128):
                price = price.to_decimal()

            # Ensure quantity is a valid number
            qty = item.quantity or 0

            total += price * qty
            quantity += qty

    except Cart.DoesNotExist:
        cart_items = []

    return {
        "cart_items": cart_items,
        "total": total,
        "quantity": quantity,
    }
