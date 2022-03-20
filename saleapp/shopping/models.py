from email.policy import default
from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    slug = AutoSlugField(unique=True, populate_from='name',
                         editable=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    thumbnail = models.ImageField(default='default.png', blank=True)
    # active
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    # category_id
    # receipt_details id

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# python manage.py makemigrations
# python manage.py migrate
