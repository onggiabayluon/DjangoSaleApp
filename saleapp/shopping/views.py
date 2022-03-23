import json

import stripe
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .models import Order, OrderItem, Payment, Product, ShippingAddress

stripe.api_key = settings.STRIPE_SECRET_KEY


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
    # >>> Render Checkout View
    if request.method == 'GET':
        try:
            if request.user.is_authenticated:
                customer = request.user.customer
                order = Order.objects.get(customer=customer, complete=False)
                items = order.orderitem_set.all()
            else:
                items = []
                order = {'get_cart_total': 0, 'get_cart_count': 0}

            context = {
                'title': 'Checkout',
                'items': items,
                'order': order,
                'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
            }
            
            return render(request, 'shopping/checkout.html', context)

        except ObjectDoesNotExist:
            messages.info(request, "Customer does not have any order.")
            return redirect("shopping:cart")

        
    
    # >>> Handling Stripe Payment
    if request.method == 'POST':
        customer = request.user.customer
        order = Order.objects.get(customer=customer, complete=False)
        token = request.POST.get('stripeToken')
        amount = int(order.get_cart_total * 100)

        try: 
            charge = stripe.Charge.create(
                amount=amount,  # cent
                currency="usd",
                source=token,
            )
            # Create The Payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.customer = customer
            payment.amount = amount
            payment.save()

            # Assign The Payment to the order
            order.complete = True
            order.payment = payment
            order.save()

            messages.success(request, "Your order was successful!")
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            messages.warning(request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.warning(
                request, "A serious error occurred. We have been notifed.")
            return redirect("/")


        


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


def process_order(request):
    data = json.loads(request.body)

    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order = Order.objects.get(id=data['order']['id'], customer=customer, complete=False)

            shipping_address = ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

            order.shipping_address = shipping_address
            order.save()
        except ObjectDoesNotExist:
            messages.info(request, "This order does not exist.")
            return redirect("shopping:cart")
            

    # return JsonResponse("Order Saved in database", safe=False)

