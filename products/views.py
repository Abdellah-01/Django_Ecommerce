from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from abdellah_collections.models import Collection
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from .models import Product, ReviewRating
from django.core.paginator import Paginator
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct

# -------------------------------
# Product List View
# -------------------------------
def product_list(request):
    all_products = Product.objects.filter(is_available=True).order_by("-created_at")
    product_count = all_products.count()

    # Paginator
    page_number = request.GET.get("page", 1)
    paginator = Paginator(all_products, 12)  # 12 products per page
    page_obj = paginator.get_page(page_number)

    context = {
        "all_products": page_obj,
        "product_count": product_count,
    }
    return render(request, "products/product-list.html", context)


# -------------------------------
# Product Details View
# -------------------------------
def product_details(request, product_slug):
    single_product = get_object_or_404(Product, slug=product_slug)

    size_guide = single_product.size_guide
    cm_table = size_guide.get_cm_table() if size_guide else None
    related_products = (
        Product.objects.filter(collection=single_product.collection)
        .exclude(id=single_product.id)[:10]
    )

    in_cart = CartItem.objects.filter(
        cart__cart_id=_cart_id(request), product=single_product
    ).exists()

    # ✅ Prepare size-stock mapping and total stock
    size_stock = {}
    total_stock = 0
    if hasattr(single_product, "sizes") and single_product.sizes:
        for size in single_product.sizes:
            stock = single_product.stock_for_size(size)
            size_stock[size] = stock
            total_stock += stock  # accumulate total stock

    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(
                user=request.user,
                product_id=single_product.id
            ).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None
    
    # Get Reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "related_products": related_products,
        "size_guide": size_guide,
        "cm_table": cm_table,
        "size_stock": size_stock,        # stock per size
        "has_stock": total_stock > 0,    # ✅ boolean for template
        "order_product": order_product,
        "reviews": reviews,
    }

    return render(request, "products/product-details.html", context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            review = ReviewRating.objects.get(user_id=request.user.id, product_id=product_id)
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, "Thank You! Your Review Has Been Updated")
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.user_id = request.user.id
                new_review.product_id = product_id
                new_review.ip = request.META.get('REMOTE_ADDR')
                new_review.save()
                messages.success(request, "Thank You! Your Review Has Been Submitted")
    return redirect(url)
