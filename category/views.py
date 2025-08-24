from django.shortcuts import render, get_object_or_404
from .models import Category
from products.models import Product
from django.core.paginator import Paginator

def category_list(request):
    all_category = list(Category.objects.all())
    
    # Split categories into chunks of 3 for template
    chunks = [all_category[i:i + 3] for i in range(0, len(all_category), 3)]
    
    context = {
        'chunks': chunks,  # pass the chunks to template
    }
    return render(request, 'category/category.html', context)

def category_products(request, category_slug=None):
    categories = None
    all_products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        all_products = Product.objects.filter(category=categories, is_available__in=[True])
        product_count = all_products.count()

    else:
        all_products = Product.objects.all().filter(is_available__in=[True])
        product_count = all_products.count()
    
    paginator = Paginator(all_products, 3)  # 8 products per page
    page_number = request.GET.get('page')
    all_products = paginator.get_page(page_number)

    context = {
        'all_products':all_products,
        'product_count':product_count,
        'categories':categories,
    }
    return render(request, 'category/product-list.html', context)
