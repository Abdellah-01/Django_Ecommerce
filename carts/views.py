from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from decimal import Decimal
from bson.decimal128 import Decimal128
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    selected_size = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))

    # ✅ get stock for this variant
    stock = product.stock_for_size(selected_size) if selected_size else 0

    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product=product, user=request.user, size=selected_size)
            if cart_item.quantity + quantity <= stock:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = stock
            cart_item.save()
        except CartItem.DoesNotExist:
            if quantity > stock:
                quantity = stock
            cart_item = CartItem.objects.create(
                product=product,
                user=request.user,
                size=selected_size,
                quantity=quantity
            )
            cart_item.save()

    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart, size=selected_size)
            if cart_item.quantity + quantity <= stock:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = stock
            cart_item.save()
        except CartItem.DoesNotExist:
            if quantity > stock:
                quantity = stock
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
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        else:
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
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        else:
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

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        except ObjectDoesNotExist:
            cart_items = []

    # attach available stock per variant
    for item in cart_items:
        if item.size:
            item.available_stock = item.product.stock_for_size(item.size)
        else:
            item.available_stock = 0

        price = to_decimal(item.product.price)
        qty = item.quantity or 0
        total += price * qty
        quantity += qty

    tax = (Decimal('5') * total) / Decimal('100')
    platform_fee = Decimal('12.00')
    grand_total = total + platform_fee

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

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        except ObjectDoesNotExist:
            cart_items = []

    for item in cart_items:
        if item.size:
            item.available_stock = item.product.stock_for_size(item.size)
        else:
            item.available_stock = 0

        price = to_decimal(item.product.price)
        qty = item.quantity or 0
        total += price * qty
        quantity += qty

    tax = (Decimal('5') * total) / Decimal('100')
    platform_fee = Decimal('12.00')
    grand_total = total + platform_fee

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'platform_fee': platform_fee,
        'grand_total': grand_total,
    }
    return render(request, 'carts/shop_checkout.html', context)
