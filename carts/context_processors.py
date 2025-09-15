from decimal import Decimal
from bson.decimal128 import Decimal128
from .models import Cart, CartItem
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist

def cart_context(request):
    cart_items = []
    total = Decimal('0.00')
    quantity = 0

    try:
        if request.user.is_authenticated:
            # 🔑 Logged-in user's cart
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            # 🔑 Guest cart
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    except ObjectDoesNotExist:
        cart_items = []

    for item in cart_items:
        # Convert price to Decimal safely
        price = item.product.price
        if isinstance(price, Decimal128):
            price = price.to_decimal()

        qty = item.quantity or 0
        total += price * qty
        quantity += qty

        # ✅ Attach available stock to each cart_item (Newly Added)
        if item.size:
            item.available_stock = item.product.stock_for_size(item.size)
        else:
            item.available_stock = 0

    return {
        "cart_items": cart_items,
        "total": total,
        "quantity": quantity,
    }
