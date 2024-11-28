# shop/context_processors.py
from .models import Cart
from .models import Product, Category
from django.db.models import Avg, Count
from django.core.cache import cache

def cart_count(request):
    if request.user.is_authenticated:
        # cart_count = Cart.objects.filter(user=request.user).count()
        cart_count = 0
    else:
        cart_count = 0
    return {'cart_count': cart_count}

def global_footer_context(request):
    category_list = Category.objects.all()
    return {'category_list': category_list}

def global_product_context(request):
    filtered_products = Product.objects.filter(is_show=1).order_by('?')[:5]
    cache.set('random_products', filtered_products, 300)
    return {'filtered_products': filtered_products}