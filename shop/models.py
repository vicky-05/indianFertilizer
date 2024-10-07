from django.db import models
import datetime
import os
from django.contrib.auth.models import User

def getFilename(request, filename): 
    now_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    new_filename = "%s%s" % (now_time, filename)
    return os.path.join('uploads/', new_filename)

class trend_products(models.Model):
    product_top_title = models.CharField(max_length=255,null=False,blank=False)
    product_img = models.ImageField(upload_to=getFilename,null=True,blank=True)
    product_title = models.CharField(max_length=255)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    disc_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_decrip = models.TextField(max_length=5000,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0=show,1=Hidden")
    trend = models.BooleanField(default=False,help_text="0=default,1=trend")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_title

class Category(models.Model):
    product_title = models.CharField(max_length=255,null=False,blank=False)
    product_img = models.ImageField(upload_to=getFilename,null=True,blank=True)
    status = models.BooleanField(default=False,help_text="0=show,1=Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_title

class TopBrands(models.Model):
    product_title = models.CharField(max_length=255,null=False,blank=False)
    product_img = models.ImageField(upload_to=getFilename,null=True,blank=True)
    status = models.BooleanField(default=False,help_text="0=show,1=Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_title

class productCollection(models.Model):
    group_name = models.CharField(max_length=255,null=True,blank=True)
    brand_name = models.CharField(max_length=255,null=True,blank=True)
    name_product = models.CharField(max_length=255)
    image_product = models.ImageField(upload_to=getFilename,null=True,blank=True)
    image_product_2 = models.ImageField(upload_to=getFilename,null=True,blank=True)
    mrp_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    quantity = models.IntegerField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    benefits = models.TextField(null=True,blank=True)
    recommendations = models.TextField(null=True,blank=True)
    technical_specifications = models.TextField(null=True, blank=True)
    demonstration_video = models.URLField(null=True,blank=True,help_text="0=show,1=Hidden")
    status = models.BooleanField(default=False,help_text="0=show,1=Hidden")
    created_at = models.DateTimeField(auto_now_add=True)
    slug= models.SlugField(max_length=255,null=True,blank=True)
    trending = models.BooleanField(default=False,help_text="0=default,1=trend")

    def __str__(self):
        return self.name_product

    def save(self, *args, **kwargs):
        # Calculate discount percentage
        if self.mrp_price > 0:
            self.discount_percentage = ((self.mrp_price - self.discounted_price) / self.mrp_price) * 100
        else:
            self.discount_percentage = 0

        # Calculate discount amount
        self.discount_amount = self.mrp_price - self.discounted_price

        super().save(*args, **kwargs)


class Price(models.Model):
    product = models.ForeignKey('productCollection', on_delete=models.CASCADE, related_name='prices')
    quantity = models.CharField(max_length=10)  # You can adjust this field based on your requirements
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(productCollection, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.product_qty * self.product.discounted_price
    @property
    def discounted_total_cost(self):
        return self.product_qty * self.product.discount_amount

