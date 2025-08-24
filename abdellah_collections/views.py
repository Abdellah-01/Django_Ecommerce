from django.shortcuts import render, get_object_or_404
from .models import Collection
from products.models import Product
from django.core.paginator import Paginator

# Create your views here.
def collections_list(request):
    all_collections = Collection.objects.all()
    context = {
        'all_collections':all_collections,
    }
    return render(request, 'collections/collections.html', context)

def all_products_collections(request, collection_slug=None):
    collections = None
    all_products = None

    if collection_slug != None:
        collections = get_object_or_404(Collection, slug=collection_slug)
        all_products = Product.objects.filter(collection=collections, is_available__in=[True])
        product_count = all_products.count()
        
    else:
        all_products = Product.objects.all().filter(is_available__in=[True])
        product_count = all_products.count()

    # ADD PAGINATOR
    paginator = Paginator(all_products, 3)  # 8 products per page
    page_number = request.GET.get('page')
    all_products = paginator.get_page(page_number)

    context = {
        'all_products':all_products,
        'product_count':product_count,
        'collections':collections,
    }
    return render(request, 'collections/product-list.html', context)