from django.http import HttpResponse
from django.shortcuts import render
from .models import Product


def shopping_list(request):
    products = Product.objects.all().order_by('created_at')
    return render(request, 'shopping/shopping_list.html', {
        'title': 'Products', 
        'products': products
    })


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'shopping/product_detail.html', {
        'title': product.name,
        'product': product
    })
