from . models import Collection

def menu_links(request):
    clinks = Collection.objects.all()
    return dict(clinks=clinks)