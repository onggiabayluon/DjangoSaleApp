from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

    @receiver(post_save, sender=User)
    def create_customer(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance, name=instance.username)


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
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey('payment', on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        cart_total = sum([order_item.get_total for order_item in order_items])
        return cart_total
    
    @property
    def get_cart_count(self):
        order_items = self.orderitem_set.all()
        cart_count = sum([order_item.quantity for order_item in order_items])
        return cart_count


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if type(self.address) != type(None):
            return "Customer - " + self.customer.name + " | Shipping - " + self.address
        else:
            return "Customer - " + self.customer.name


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    thumbnail = models.ImageField(
        default='default.png', blank=True, upload_to='categories/%Y/%m')

    def __str__(self):
        return self.name

# python manage.py makemigrations
# python manage.py migrate
