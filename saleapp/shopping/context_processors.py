from .models import Order

def get_cart_count(request):
    order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
    return {'cart_count': order.get_cart_count}
