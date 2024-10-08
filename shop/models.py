from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    mobile_no = models.BigIntegerField(default=0, validators=[MinValueValidator(11111111111), MaxValueValidator(9999999999)])
    profile_img = models.ImageField(upload_to='customer_profile_images/', default='customer_profile_images/default_img.png')

    def __str__(self):
        return self.username

class Unit(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    decrption = models.TextField()

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_unit = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    unit_of_messure = models.ForeignKey(Unit, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_trend = models.BooleanField(default=False, help_text='0 = Default, 1 = Trend')
    application = models.TextField()
    stock_qty = models.IntegerField(default=0)
    mrp_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    selling_price =  models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, editable=False)
    discount_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)

    def __str__(self):
        return self.id
    