from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.urls import reverse
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
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
            auth_login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("abdellah_shoping:home_page")  # change this
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "accounts/login.html")  # keep form data
    return render(request, "accounts/login.html")

@login_required(login_url='accounts:login_page')
def logout(request):
    auth_logout(request)
    return redirect('products:products_page')

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

