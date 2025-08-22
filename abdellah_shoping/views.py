from django.shortcuts import render

# Create your views here.
def home(request):
    header_type = 'header-transparent-bg'

    context = {
        'header_type':header_type
    }
    return render(request, 'abdellah_shoping/index.html', context)