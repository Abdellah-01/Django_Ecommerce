from django.shortcuts import render, redirect
from django.http import HttpResponse
from decimal import Decimal
from bson.decimal128 import Decimal128
import datetime, json
from django.contrib.auth.decorators import login_required
from carts.models import CartItem
from .forms import OrderForm, Order
from .models import Order, Payment, OrderProduct


def to_decimal(value):
    """Convert Decimal128 or other numeric values to Python Decimal."""
    if isinstance(value, Decimal128):
        return value.to_decimal()
    return Decimal(str(value))


@login_required
def place_order(request, total=Decimal('0.00'), quantity=0):
    current_user = request.user   # ✅ must be logged in

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('products:products_page')
    
    grand_total = Decimal('0.00')
    tax = Decimal('0.00')
    platform_fee = Decimal('0.00')
    
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
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user   # ✅ Always assign logged-in user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.mobile_number = form.cleaned_data['mobile_number']
            data.email = form.cleaned_data['email']
            data.company_name = form.cleaned_data['company_name']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pincode = form.cleaned_data['pincode']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.platform_fee = platform_fee
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # ✅ keep your existing Order ID logic
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  #20250905
            order_number = "AC" + current_date + str(data.id)  # Example: AC20250905123
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'tax':tax,
                'platform_fee':platform_fee,
                'total':total,
                'grand_total':grand_total,
            }

            return render(request, 'carts/shop_review.html', context)
        
        else:
            print("Failed")
            return redirect('carts_urls:checkout_page')
        
    return redirect('carts_urls:checkout_page')


def make_payment(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status']        
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move Cart Items to Order Product TAble
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.size = item.size or ''
        orderproduct.quantity = item.quantity
        orderproduct.product_price = Decimal(item.product.price)
        orderproduct.ordered = True
        orderproduct.save()


        # Reduce Stocks of the Sold Product
        product = item.product
        if item.size:
            normalized_size = str(item.size).lower().strip()
            size_field = f"stock_{normalized_size}"
            if hasattr(product, size_field):
                current_stock = getattr(product, size_field) or 0
                new_stock = max(current_stock - item.quantity, 0)
                setattr(product, size_field, new_stock)
                product.save()   # <<--- IMPORTANT: persist change to DB
            else:
                # helpful debug message — you can replace prints with logging
                print(f"Warning: product {product.id} has no field '{size_field}'")
        else:
            # if you later add a general stock field, handle it here
            if hasattr(product, "stock"):
                product.stock = max((getattr(product, "stock") or 0) - item.quantity, 0)
                product.save()

    # Clear the Cart
    CartItem.objects.filter(user=request.user).delete()

    # Send the Order Recieved Email to Customer

    # Send Order Number and Transaction ID Back to sendData Method Via JSON Response

    return render(request, 'carts/shop_review.html')