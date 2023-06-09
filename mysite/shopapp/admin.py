from django.contrib import admin

from shopapp.models import Product, Category, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = "name", "category", "image", "description", "price", "stock"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = "title", "active"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = "user", "product", "author", "email", "text", "rate", "date"
