from .models import Order

def get_cart_count(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
        cart_count = order.get_cart_count
    else:
        cart_count = 0

    return {'cart_count': cart_count}
