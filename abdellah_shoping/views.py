from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'abdellah_shoping/index.html')