from django.shortcuts import render
from .models import Order, OrderItem, Product
from django.http import JsonResponse
import json


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
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_count': 0}

    context = {'title': 'Checkout', 'items': items, 'order': order}
    return render(request, 'shopping/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(product=product, order=order)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove': 
        orderItem.quantity = (orderItem.quantity - 1)
    

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    # Get updated cart count
    cart_count = order.get_cart_count
    return JsonResponse({'cart_count': cart_count})


def update_item_quantity(request):
    data = json.loads(request.body)
    productId = data['productId']
    quantity = data['quantity']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(product=product, order=order)
    orderItem.quantity = quantity
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    # Get updated cart count
    cart_count = order.get_cart_count
    item_total = orderItem.get_total
    cart_total = order.get_cart_total

    return JsonResponse({
        'cart_count': cart_count,
        'item_total': item_total,
        'cart_total': cart_total
    })


def delete_item(request):
    data = json.loads(request.body)
    productId = data['productId']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(product=product, order=order)
    orderItem.delete()


    # Get updated cart count
    cart_count = order.get_cart_count
    item_total = orderItem.get_total
    cart_total = order.get_cart_total

    return JsonResponse({
        'cart_count': cart_count,
        'item_total': item_total,
        'cart_total': cart_total
    })
