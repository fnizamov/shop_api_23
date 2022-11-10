from django.contrib import admin

from .models import (
    Category,
    Product,
    ProductImage
)


class TabularInLineImages(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ['image']

class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [TabularInLineImages]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)