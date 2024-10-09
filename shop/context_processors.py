# shop/context_processors.py

from .models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        # cart_count = Cart.objects.filter(user=request.user).count()
        cart_count = 0
    else:
        cart_count = 0
    return {'cart_count': cart_count}
