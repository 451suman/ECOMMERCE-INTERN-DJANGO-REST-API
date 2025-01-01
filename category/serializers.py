from rest_framework import serializers
from category.models import Category

# class ParentCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    parent_category = serializers.SlugRelatedField( slug_field="name", queryset=Category.objects.all(), required=False) 
    class Meta: 
        model = Category
        fields = '__all__'
