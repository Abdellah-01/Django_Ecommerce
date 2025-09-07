from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.urls import reverse
from orders.models import Order, OrderProduct, Payment
from carts.models import Cart, CartItem
from carts.views import _cart_id
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
import requests

# Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = email.split("@")[0]
            mobile_number = form.cleaned_data['mobile_number']
            password = form.cleaned_data['password']

            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password
            )
            user.mobile_number = mobile_number
            # user.is_active = True 
            user.save()

            # User Activation
            current_site = get_current_site(request)
            mail_subject = "Activate Your Account"
            message = render_to_string('accounts/account_verfication_email.html', {
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_email =email
            send_email = EmailMessage(mail_subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email])
            send_email.send()
            # messages.success(request, "Please Activate Your Account!")
            return redirect(f"{reverse('accounts:login_page')}?command=verification&email={email}")

    else:
        form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            try:
                # Find guest cart
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart)

                if cart_items.exists():
                    for item in cart_items:
                        # Look for same product+size in user cart
                        existing_item = CartItem.objects.filter(
                            user=user,
                            product=item.product,
                            size=item.size
                        ).first()

                        if existing_item:
                            # Merge quantities
                            existing_item.quantity += item.quantity
                            existing_item.save()
                            item.delete()
                        else:
                            # Assign item to logged-in user
                            item.user = user
                            item.cart = None   # 🔑 detach from guest cart
                            item.save()

                # # delete guest cart after merging
                # cart.delete()

                # remove session cart_id
                if "cart_id" in request.session:
                    del request.session["cart_id"]

            except Cart.DoesNotExist:
                pass

            auth_login(request, user)
            messages.success(request, "You are now logged in.")
            # Dynamic Login Page
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                
            except:
                return redirect("accounts:dashboard_page") 
            
            
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "accounts/login.html")
    return render(request, "accounts/login.html")

def lost_password(request):
    email_error = None  # default

    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Send Email
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string('accounts/reset_pwd_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            send_email = EmailMessage(mail_subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
            send_email.send()
            messages.success(request, "Reset Email Sent Successfully!")
            return redirect('accounts:login_page')
        else:
            email_error = "User with this email does not exist!"

    return render(request, 'accounts/lost_password.html', {'email_error': email_error})


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reset Your Password')
        return redirect('accounts:reset_password_page')
    
    else:
        messages.error(request, 'This Link Has Been Expired')
        return redirect('accounts:login_page')
    
def reset_password(request):
    password_error = None
    confirm_error = None

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation
        if not password:
            password_error = "Password is required."
        elif len(password) < 6:
            password_error = "Password must be at least 6 characters."

        if not confirm_password:
            confirm_error = "Please confirm your password."
        elif password and password != confirm_password:
            confirm_error = "Passwords do not match."

        # If errors exist → re-render form
        if password_error or confirm_error:
            return render(request, 'accounts/reset_password.html', {
                'password_error': password_error,
                'confirm_error': confirm_error,
            })

        # If no errors → save new password
        uid = request.session.get('uid')
        user = Account.objects.get(pk=uid)
        user.set_password(password)
        user.save()

        messages.success(request, 'Password Reset Successful')
        return redirect('accounts:login_page')

    return render(request, 'accounts/reset_password.html')

@login_required(login_url='accounts:login_page')
def logout(request):
    auth_logout(request)
    return redirect("abdellah_shoping:home_page")

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account Activated Successfully!')
        return redirect('accounts:login_page')
    else:
        messages.error(request, 'Invalid Activation Link!')
        return redirect('accounts:register_page')

@login_required(login_url='accounts:login_page')
# User SHopping Accounts
def dashboard(request):
    active = "menu-link_active"
    context = {
        'active':active
    }
    return render(request, 'accounts/account_dashboard.html', context)

@login_required(login_url='accounts:login_page')
def my_orders(request):
    active1 = "menu-link_active"
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    orders = orders.prefetch_related('orderproduct_set')

    context = {
        'active1':active1,
        'orders':orders,
    }
    return render(request, 'accounts/account_orders.html', context)