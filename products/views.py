from django.shortcuts import render
from django.http import HttpResponse
from abdellah_collections.models import Collection
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from .models import Product
from django.core.paginator import Paginator

# Create your views here.

def product_list(request):
    all_products = Product.objects.filter(is_available__in=[True])
    product_count = all_products.count()

    # Paginator
    page_number = request.GET.get('page', 1)  # Get the page number from query params, default 1
    paginator = Paginator(all_products, 3)    # Show 8 products per page
    page_obj = paginator.get_page(page_number)

    context = {
        "all_products": page_obj,
        "product_count": product_count,
    }
    return render(request, "products/product-list.html", context)

def product_details(request, product_slug):
    try:
        single_product = Product.objects.get(slug=product_slug)
        related_products = Product.objects.filter(collection=single_product.collection).exclude(id__in=[single_product.id])[:10]
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "related_products": related_products,
    }
    return render(request, "products/product-details.html", context)

