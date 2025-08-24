from django.shortcuts import render
from abdellah_collections.models import Collection
from category.models import Category
from products.models import Product
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def home(request):
    header_type = 'header-transparent-bg'

    context = {
        'header_type':header_type,

    }
    return render(request, 'abdellah_shoping/index.html', context)

def search(request):
    if 'search-keyword' in request.GET:
        keyword = request.GET['search-keyword']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
            product_count = products.count()
            

    context = {
        'all_products': products,
        'keyword': keyword,
        'product_count': product_count,
    }
    return render(request, 'abdellah_shoping/search.html', context)