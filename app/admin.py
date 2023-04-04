from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Product)
class ProductModeAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','product_image']