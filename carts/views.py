from django.shortcuts import render

# Create your views here.
def view_cart(request):
    return render(request, 'carts/shop_cart.html')