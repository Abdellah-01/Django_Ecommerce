from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from decimal import Decimal
from bson.decimal128 import Decimal128
from django.http import JsonResponse

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    quantity = request.GET['quantity']
    size = request.GET['size']
    return HttpResponse(f"Quantity: {quantity}, Size: {size}")
    exit()
    product = Product.objects.get(id=product_id) # get The Product
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session

    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1 # increase the cart item quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    # return HttpResponse(cart_item.quantity)
    # exit()
    return redirect('carts_urls:view_cart_page')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass  # or redirect with a message
    
    return redirect('carts_urls:view_cart_page')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  # or redirect with a message
    
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
        grand_total = total + tax + platform_fee

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
