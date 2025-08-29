from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from decimal import Decimal
from bson.decimal128 import Decimal128
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    selected_size = request.POST.get('size')   # ✅ size comes from form
    quantity = int(request.POST.get('quantity', 1))

    # get or create cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    # get or create cart item (match product + cart + size)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, size=selected_size)
        # ✅ check stock before increasing
        if cart_item.quantity + quantity <= product.stock:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = product.stock
        cart_item.save()
    except CartItem.DoesNotExist:
        if quantity > product.stock:
            quantity = product.stock
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            size=selected_size,
            quantity=quantity
        )
        cart_item.save()

    return redirect('carts_urls:view_cart_page')



def remove_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__cart_id=_cart_id(request))
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('carts_urls:view_cart_page')



def remove_cart_item(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__cart_id=_cart_id(request))
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('carts_urls:view_cart_page')



def to_decimal(value):
    """Convert Decimal128 or other numeric values to Python Decimal."""
    if isinstance(value, Decimal128):
        return value.to_decimal()
    return Decimal(str(value))

def view_cart(request):
    total = Decimal('0.00')
    quantity = 0
    tax = Decimal('0.00')
    platform_fee = Decimal('0.00')
    grand_total = Decimal('0.00')
    cart_items = []

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active__in=[True])

        for cart_item in cart_items:
            # Convert price to Decimal safely
            price = to_decimal(cart_item.product.price)
            
            # Ensure quantity is never None
            qty = cart_item.quantity or 0

            total += price * qty
            quantity += qty

        tax = (Decimal('5') * total) / Decimal('100')   # 5% tax
        platform_fee = Decimal('12.00')
        grand_total = total + platform_fee

    except ObjectDoesNotExist:
        cart_items = []

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'platform_fee': platform_fee,
        'grand_total': grand_total,
    }

    return render(request, 'carts/shop_cart.html', context)

@login_required(login_url='accounts:login_page')
def checkout(request):
    total = Decimal('0.00')
    quantity = 0
    tax = Decimal('0.00')
    platform_fee = Decimal('0.00')
    grand_total = Decimal('0.00')
    cart_items = []

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active__in=[True])

        for cart_item in cart_items:
            # Convert price to Decimal safely
            price = to_decimal(cart_item.product.price)
            
            # Ensure quantity is never None
            qty = cart_item.quantity or 0

            total += price * qty
            quantity += qty

        tax = (Decimal('5') * total) / Decimal('100')   # 5% tax
        platform_fee = Decimal('12.00')
        grand_total = total + platform_fee

    except ObjectDoesNotExist:
        cart_items = []

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'platform_fee': platform_fee,
        'grand_total': grand_total,
    }

    return render(request, 'carts/shop_checkout.html', context)