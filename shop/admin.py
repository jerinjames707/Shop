from django.contrib import admin
from shop.models import Product, Order, Cart, Review

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Review)