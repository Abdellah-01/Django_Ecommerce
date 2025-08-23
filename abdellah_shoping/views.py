from django.shortcuts import render
from abdellah_collections.models import Collection
from category.models import Category

all_collections = Collection.objects.all()
all_category = Category.objects.all()

# Create your views here.
def home(request):
    header_type = 'header-transparent-bg'

    context = {
        'header_type':header_type,
        'all_collections':all_collections,
        'all_category':all_category,

    }
    return render(request, 'abdellah_shoping/index.html', context)