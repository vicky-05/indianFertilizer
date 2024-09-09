from django.contrib import admin
from .models import *

admin.site.register(trend_products)
admin.site.register(Category)
admin.site.register(TopBrands)
admin.site.register(productCollection)
admin.site.register(Price)
admin.site.register(Cart)

