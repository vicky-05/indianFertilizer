from django.urls import path
from shop import views

urlpatterns = [
    path('', views.home,name='home'),
    path('about',views.about,name='about'),
    path('search/', views.search_view, name='search'),
    path('product_details/<int:product_id>', views.product_details, name='product_details'),
    path('categories', views.categories,name='categories'),
    # path('collections', views.collections,name='collections'),
    # path('collections/<str:group_name>', views.collectionsview,name='collections'),
    # path('collections/<str:cname>/<str:pname>', views.product_details, name='product_details'),
    path('add_to_cart/<int:product_id>', views.add_to_cart,name='add_to_cart'),
    path('cart', views.cart_page,name='cart'),
    # path('remove_cart/<str:cid>', views.remove_cart,name='remove_cart'),
    # path('cart/<str:pnme>', views.product_detailss, name='product_detailss'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
    path('load_more_reviews/', views.load_more_reviews, name='load_more_reviews'),
]