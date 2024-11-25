from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from shop.models import *


@receiver(pre_save, sender=Category)
def unique_category_slug_generator(sender, instance, **kwargs):
    # Generate the Slug
    base_slug = slugify(instance.name)
    slug = base_slug
    counter = 1
    while Category.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    instance.slug = slug

@receiver(pre_save, sender=Product)
def unique_product_slug_generator(sender, instance, **kwargs):
    # Generate the Slug
    base_slug = slugify(instance.name)
    slug = base_slug
    counter = 1
    while Product.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    instance.slug = slug

    # Calculate discount price
    if instance.mrp_price > 0:
        instance.discount_price = instance.mrp_price * instance.discount_percentage // 100
    else:
        instance.discount_price = 0
    # Calculate selling amount
    instance.selling_price = instance.mrp_price - instance.discount_price