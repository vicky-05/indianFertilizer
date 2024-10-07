from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from django.contrib.auth.models import User


class Unit(models.Model):
    name = models.CharField(max_length=255)

class Brand(models.Model):
    name = models.charField(max_length=255)

class Categorys(MPTTModel):
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
    price_per_unit = models.IntegerField()
    weight = models.IntegerField()
    unit_of_messure = models.ForeignKey(Unit, on_delete=models.SET_NULL)
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_trend = models.BooleanField(related_name="0-not, 1-trend", default=0)
    application = models.TextField()
    stock_qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Add2Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    