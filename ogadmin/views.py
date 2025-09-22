from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from .forms import AdminLoginForm
from accounts.models import Account
from products.models import Product
from abdellah_collections.models import Collection
from category.models import Category

# Authentication
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

# Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None and getattr(user, 'is_superadmin', False):
                auth_login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect('ogadmin:dashboard_admin_page')
            else:
                messages.error(request, "Invalid email/password or not authorized.")
        else:
            messages.error(request, "Please fill in all fields correctly.")
    else:
        form = AdminLoginForm()

    return render(request, 'ogadmin/auth-login.html', {'form': form})

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Account.objects.get(email__exact=email, is_superadmin=True)
        except Account.DoesNotExist:
            user = None

        if user is not None and getattr(user, 'is_superadmin', False):
            # Send reset email only to superadmin users
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password (Super Admin)"
            message = render_to_string('accounts/reset_pwd_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            send_email = EmailMessage(
                mail_subject,
                message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            send_email.send()
            messages.success(request, "Reset email sent successfully!")
            return redirect('ogadmin:login_admin_page')
        else:
            messages.error(request, "Super admin account with this email does not exist!")

    return render(request, 'ogadmin/auth-pass-reset.html')

@login_required(login_url='ogadmin:login_admin_page')
def logout(request):
    auth_logout(request)
    return redirect("ogadmin:login_admin_page")

@login_required(login_url='ogadmin:login_admin_page')
def dashboard(request):
    active = 'active'

    context = {
        active : 'active'
    }
    return render(request, 'ogadmin/index.html', context)

@login_required(login_url='ogadmin:login_admin_page')
def products(request):
    all_products = Product.objects.all().order_by("-created_at")
    all_collections = Collection.objects.all()
    all_categories = Category.objects.all()
    product_count = all_products.count()

    context = {
        'all_products': all_products,
        'product_count': product_count,
        'all_collections': all_collections,
        'all_categories': all_categories,
    }

    return render(request, 'ogadmin/product-list.html', context)

@login_required(login_url='ogadmin:login_admin_page')
def view_product(request, product_slug):
    # Fetch product by slug or return 404
    product = get_object_or_404(Product, slug=product_slug)

    # Optional: if you want related collections/categories
    collections = Collection.objects.all()
    categories = Category.objects.all()

    context = {
        'product': product,
        'collections': collections,
        'categories': categories,
    }

    return render(request, 'ogadmin/product-details.html', context)


def collections(request):
    collections = Collection.objects.all().order_by('-id')

    context = {
        'collections': collections,
    }
    return render(request, 'ogadmin/collection.html', context)

def categories(request):
    categories = Category.objects.all().order_by('-id')

    context = {
        'categories': categories,
    }

    return render(request, 'ogadmin/categories.html', context)