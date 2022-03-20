from django.http import HttpResponse
from django.shortcuts import render

from shopping.models import Product


def homepage(request):
    products = Product.objects.all()
    return render(request, 'homepage.html', {
        'title': 'Home', 'products': products
    })
