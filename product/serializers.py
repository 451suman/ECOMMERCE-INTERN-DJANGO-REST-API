from rest_framework import serializers
from category.models import Category
from product.models import Product
from category.serializers import CategorySerializer
import base64
from django.core.files.base import ContentFile

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



class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # Only expect an ID
    image = serializers.CharField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "description",
            "price",
            "image",
            "image_url",
        ]

    def get_image_url(self, obj):
        if obj.image:
            with open(obj.image.path, "rb") as image_file:
                return f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode()}"
        return None

    def create(self, validated_data):
        image_data = validated_data.pop("image", None)

        if image_data:
            format, imgstr = image_data.split(";base64,")
            ext = format.split("/")[-1]
            file_name = f"{validated_data['name']}.{ext}"
            validated_data["image"] = ContentFile(base64.b64decode(imgstr), name=file_name)

        product = Product.objects.create(**validated_data)
        return product



# class ProductWriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = [
#             "name",
#             "category",
#             "description",
#             "price",
#             "image",
#         ]