from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from django.core.validators import MaxValueValidator
from authendicate.models import User
import datetime
import os

def getFilename(request, filename): 
    now_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    new_filename = "%s%s" % (now_time, filename)
    return os.path.join('product_and_category_images/', new_filename)

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
    image = models.ImageField(upload_to=getFilename)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    decrption = models.TextField()

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=getFilename)
    image1 =models.ImageField(upload_to=getFilename, null=True, blank=True)
    image2 = models.ImageField(upload_to=getFilename, null=True, blank=True)
    weight = models.IntegerField(default=0)
    unit_of_messure = models.ForeignKey(Unit, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_show = models.BooleanField(default=True, help_text='0 = Not show, 1 = Default')
    is_trend = models.BooleanField(default=False, help_text='0 = Default, 1 = Trend')
    view_count = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    stock_qty = models.IntegerField(default=0, blank=True)
    mrp_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    selling_price =  models.DecimalField(default=0.0, max_digits=10, decimal_places=2, editable=False)
    discount_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, editable=False)
    demo_url = models.URLField(null=True, blank=True)
    recommandation = models.TextField(null=True, blank=True)
    benifits_and_features = models.TextField(null=True, blank=True)
    discount_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Calculate discount price
        if self.mrp_price > 0:
            self.discount_price = self.mrp_price * self.discount_percentage // 100
        else:
            self.discount_price = 0
        # Calculate selling amount
        self.selling_price = self.mrp_price - self.discount_price
        super().save(*args, **kwargs)

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart')
    qty = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)
