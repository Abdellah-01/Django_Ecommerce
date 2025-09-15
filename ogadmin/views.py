from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import AdminLoginForm

# Authentication
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='ogadmin:login_admin_page')
def logout(request):
    auth_logout(request)
    return redirect("ogadmin:login_admin_page")

@login_required(login_url='ogadmin:login_admin_page')
def overview(request):
    return render(request, 'ogadmin/analytics.html')