from rest_framework import serializers
from .models import Product, Category


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ["id", "category", "description", "price", "count", "title", "images"]
