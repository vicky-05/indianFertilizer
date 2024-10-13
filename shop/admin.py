from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display =  [ 'username', 'mobile_no', 'profile_img' ]

class CategoryAdmin(admin.ModelAdmin):
    list_display =  [ 'name', 'parent' ]

class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'category', 'brand', 'mrp_price', 'stock_qty', 'is_trend' ]

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'product', 'rating', 'review' ]

class CartAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'product', 'qty' ]

admin.site.register(User, UserAdmin)
admin.site.register(Unit)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Cart, CartAdmin)
