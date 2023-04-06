from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html

from .models import *

# Register your models here.
@admin.register(Product)
class ProductModeAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','product_image']
@admin.register(Customer)
class CustomerModeAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']

@admin.register(Cart)
class CartModeAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']
    def product(self, obj):
        link = reverse('admin:app_product_change',args=[obj.product.pk])
        return format_html('<a href={}>{}</a>', link, obj.product.title)

@admin.register(Payment)
class PaymentModeAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorzpy_order_id','razorzpy_payment_status','paid']

@admin.register(OrderPlaced)
class OrderPlacedModeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'product', 'quantity',
        'customer', 'ordered_date', 'status', 'payment']

    def product(self, obj):
        link = reverse('admin:app_product_change',args=[obj.product.pk])
        return format_html('<a href={}>{}</a>', link, obj.product.title)
    def customer(self, obj):
        link = reverse('admin:app_customer_change',args=[obj.customer.pk])
        return format_html('<a href={}>{}</a>', link, obj.customer.title)
    def payment(self, obj):
        link = reverse('admin:app_payment_change',args=[obj.payment.pk])
        return format_html('<a href={}>{}</a>', link, obj.payment.razorzpy_payment_id)


@admin.register(WishList)
class WishListModeAdmin(admin.ModelAdmin):
    list_display = ['id','user','product']

    def product(self, obj):
        link = reverse('admin:app_product_change',args=[obj.product.pk])
        return format_html('<a href={}>{}</a>', link, obj.product.title)


admin.site.unregister(Group)