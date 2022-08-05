from django.contrib import admin
from .models import Slider, Product, Countdown, \
    Theme, Cart, Sideofferbar, ReviewRating, Customer, Wishlist, Order, OrderItem

# Register your models here.
admin.site.register(Slider)
admin.site.register(Customer)
admin.site.register(Countdown)
admin.site.register(Theme)
admin.site.register(Cart)
admin.site.register(Sideofferbar)
admin.site.register(ReviewRating)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)


class MyModelAdmin(admin.ModelAdmin):
    pass

'''
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('product_name', 'category', 'subcategory', 'Brand', 'availability', 'discounted_price',)
'''

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'discounted_price', 'prod_image')


admin.site.register(Product, ProductAdmin)
