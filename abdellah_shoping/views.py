from django.shortcuts import redirect, render
from abdellah_collections.models import Collection
from category.models import Category
from products.models import Product
from .models import ImageBanner, FAQ
from django.core.paginator import Paginator
from django.db.models import Q
from itertools import groupby
from operator import attrgetter

# Create your views here.
def home(request):
    header_type = 'header-transparent-bg'
    banners = ImageBanner.objects.all()

    context = {
        'header_type':header_type,
        'banners':banners,

    }
    return render(request, 'abdellah_shoping/index.html', context)

def search_here(request):
    all_products = Product.objects.filter(is_available=True).order_by('-created_at')[:6]

    context ={
        'all_products':all_products
    }
    return render(request, 'abdellah_shoping/search_here.html', context)

def search(request):
    if 'search-keyword' in request.GET:
        keyword = request.GET['search-keyword'].strip()  # remove extra spaces
        if keyword:  
            products = Product.objects.order_by('-created_at').filter(
                Q(product_name__icontains=keyword) | Q(description__icontains=keyword)
            )
            product_count = products.count()

            context = {
                'all_products': products,
                'keyword': keyword,
                'product_count': product_count,
            }
            return render(request, 'abdellah_shoping/search.html', context)
        else:
            # Empty keyword → redirect to homepage
            return redirect('abdellah_shoping:search_here_page')  # replace 'home' with your homepage URL name

    return redirect('abdellah_shoping:search_here_page')  # fallback if no keyword param

def faq(request):

    faqs = FAQ.objects.all().order_by("heading", "order")

    grouped_faqs = {}

    for heading, items in groupby(faqs, key=attrgetter("heading")):
        grouped_faqs[heading] = list(items)

    context = {
            "grouped_faqs": grouped_faqs
    }
    return render(request, 'abdellah_shoping/faq.html', context)
