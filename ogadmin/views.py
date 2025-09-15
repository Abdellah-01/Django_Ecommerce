from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import AdminLoginForm
from accounts.models import Account

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
                return redirect('ogadmin:overview_admin_page')
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

        if user:
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

    return render(request, 'ogadmin/auth-forget-pwd.html')

@login_required(login_url='ogadmin:login_admin_page')
def logout(request):
    auth_logout(request)
    return redirect("ogadmin:login_admin_page")

@login_required(login_url='ogadmin:login_admin_page')
def overview(request):
    return render(request, 'ogadmin/analytics.html')