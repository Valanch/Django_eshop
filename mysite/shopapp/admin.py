from django.contrib import admin

from shopapp.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = "name", "category", "image", "description", "price", "stock"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = "name", "active"
