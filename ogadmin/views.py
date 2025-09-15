from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def overview(request):
    return HttpResponse('Overview Page')