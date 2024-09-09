from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('register', views.register,name='register'),
    path('login', views.login_page,name='login'),
    path('logout', views.logout_page,name='logout'),
    path('categories', views.categories,name='categories'),
    path('collections', views.collections,name='collections'),
    path('collections/<str:group_name>', views.collectionsview,name='collections'),
    path('collections/<str:cname>/<str:pname>', views.product_details, name='product_details'),
    path('user_profile', views.user_profile,name='user_profile'),
    path('addtocart', views.add_cart,name='addtocart'),
    path('cart', views.cart_page,name='cart'),
    path('remove_cart/<str:cid>', views.remove_cart,name='remove_cart'),
    path('forgot', views.forgot_pass,name='forgot'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('cart/<str:pnme>', views.product_detailss, name='product_detailss'),


]