from rest_framework import serializers
from product.models import Product
from category.serializers import CategorySerializer



class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "description",
            "price",
            "image",
        ]
        read_only_fields = fields



class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "description",
            "price",
            "image",
        ]

