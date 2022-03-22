from django.urls import path, re_path
from . import views

app_name = 'shopping'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('update_item_quantity/', views.update_item_quantity, name='update_item_quantity'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.product_detail, name='detail'),
]
