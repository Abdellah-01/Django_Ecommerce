from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages

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
            user.save()
            messages.success(request, "Account Created successfully!")
            return redirect('accounts:login_page')  # Redirect back to the same page
    else:
        form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    pass