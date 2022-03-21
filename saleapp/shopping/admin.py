from django.contrib import admin
from .models import Category, Customer, Order, OrderItem, Product

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
