from django.shortcuts import render

# Create your views here.
def track_order(request):
    context = {}
    return render(request, 'pages/order_tracking.html', context)

def return_exchange(request):
    context = {}
    return render(request, 'pages/return_exchange.html', context)