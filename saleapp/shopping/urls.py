from django.urls import path, re_path
from . import views

app_name = 'shopping'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.product_detail, name='detail'),
]
