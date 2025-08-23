from . models import Collection

def menu_links(request):
    links = Collection.objects.all()
    return dict(links=links)