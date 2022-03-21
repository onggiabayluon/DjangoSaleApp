from autoslug import AutoSlugField
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey('Category', related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    slug = AutoSlugField(unique=True, populate_from='name', editable=True, blank=True)
    thumbnail = models.ImageField(default='default.png', blank=True, upload_to='products/%Y/%m')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    description = models.TextField(max_length=250, null=True)

    # receipt_details id

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    thumbnail = models.ImageField(
        default='default.png', blank=True, upload_to='categories/%Y/%m')

    def __str__(self):
        return self.name

# python manage.py makemigrations
# python manage.py migrate
