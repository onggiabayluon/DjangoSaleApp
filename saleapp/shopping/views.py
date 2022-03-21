from django.http import HttpResponse
from django.shortcuts import render
from .models import Product



def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    context = {'title': product.name, 'product': product}
    return render(request, 'shopping/product_detail.html', context)


def cart_view(request):
    context = {'title': 'Cart'}
    return HttpResponse('cart')
    return render(request, 'shopping/cart.html', context)


def checkout_view(request):
    context = {'title': 'Checkout'}
    return HttpResponse('checkout')
    return render(request, 'shopping/checkout.html', context)
