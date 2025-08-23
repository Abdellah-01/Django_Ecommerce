from django.shortcuts import render
from abdellah_collections.models import Collection
from category.models import Category
from .models import Product

# Create your views here.

def product_list(request):
    all_products = Product.objects.filter(is_available__in=[True])
    product_count = all_products.count()
    context = {
        "all_products": all_products,
        "product_count": product_count,
    }
    return render(request, "products/product-list.html", context)

def product_details(request, product_slug):
    try:
        single_product = Product.objects.get(slug=product_slug)
    except Exception as e:
        raise e
    context = {
        "single_product": single_product,
    }
    return render(request, "products/product-details.html", context)

