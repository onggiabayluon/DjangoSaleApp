from django.http import HttpResponse
from django.shortcuts import render
from .models import Order, Product



def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    context = {'title': product.name, 'product': product}
    return render(request, 'shopping/product_detail.html', context)


def cart_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_count': 0}
        
    context = {'title': 'Cart', 'items': items, 'order': order}
    return render(request, 'shopping/cart.html', context)


def checkout_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_count': 0}

    context = {'title': 'Checkout', 'items': items, 'order': order}
    return render(request, 'shopping/checkout.html', context)

