from django.shortcuts import render
from abdellah_collections.models import Collection
from category.models import Category
from .models import Product

# Create your views here.

all_collections = Collection.objects.all()
all_category = Category.objects.all()

def product_list(request):
    all_products = Product.objects.filter(is_available__in=[True])
    context = {
        "all_products": all_products,
        'all_collections':all_collections,
        'all_category':all_category,
    }
    return render(request, "products/product-list.html", context)

