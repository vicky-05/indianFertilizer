from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

class UserAdmin(admin.ModelAdmin):
    list_display =  [ 'username', 'mobile_no', 'profile_img' ]

class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'category', 'brand', 'mrp_price', 'discount_price', 'selling_price', 'stock_qty', 'is_trend', 'is_show', 'view_count' ]
    resource_classes = [ 'name' ]

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'product', 'rating', 'review' ]

class CartAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'product', 'qty' ]

admin.site.register(User, UserAdmin)
admin.site.register(Category, ImportExportModelAdmin)
admin.site.register(Brand, ImportExportModelAdmin)
admin.site.register(Product, ImportExportModelAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Cart, CartAdmin)
