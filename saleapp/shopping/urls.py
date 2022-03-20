from django.urls import path, re_path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.shopping_list, name='list'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.product_detail, name='detail'),
]
