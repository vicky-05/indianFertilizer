from django.urls import path
from shop import views

urlpatterns = [
    path('', views.home,name='home'),
    path('about',views.about,name='about'),
    path('search/', views.search_products, name='search'),
    path('product_details/<slug:product_slug>', views.product_details, name='product_details'),
    path('categories', views.categories,name='categories'),
    path('categories/<slug:category_slug>', views.categories,name='categories'),
    path('add_to_cart/<slug:product_slug>', views.add_to_cart,name='add_to_cart'),
    path('products/', views.products, name='products'),
    path('products/<slug:category_slug>', views.products, name='products'),
    path('get_products/', views.get_products, name='get_products'),
    path('cart', views.cart_page,name='cart'),
    path('update_product_qty/<slug:product_slug>/<str:action>', views.update_product_qty, name='update_product_qty'),
    path('add_review/<slug:product_slug>/', views.add_review, name='add_review'),
    path('load_more_reviews/', views.load_more_reviews, name='load_more_reviews'),
    
]