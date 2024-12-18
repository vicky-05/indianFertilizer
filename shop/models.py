from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from django.core.validators import MaxValueValidator
from authendicate.models import User
from django.utils.text import slugify
import datetime
import os

def getFilename(request, filename): 
    now_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    new_filename = "%s%s" % (now_time, filename)
    return os.path.join('product_and_category_images/', new_filename)

class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=getFilename)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    UNIT_CHOICES = [
    ( 'KG', 'KiloGram' ),
    ( 'G', 'Gram' ),
    ( 'MG', 'MilliGram' ),
    ( 'ML', 'MilliLiter' ),
    ( 'L', 'Liter' ),
    ( 'KL', 'KiloLiter' ),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=getFilename)
    image1 =models.ImageField(upload_to=getFilename, null=True, blank=True)
    image2 = models.ImageField(upload_to=getFilename, null=True, blank=True)
    weight = models.IntegerField(default=0)
    unit_of_messure = models.CharField(max_length=20, choices=UNIT_CHOICES)
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
    slug = models.SlugField()


    def __str__(self):
        return self.name

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
