from django.shortcuts import render
from product.models import Product
from product.serializers import ProductReadSerializer, ProductWriteSerializer
from rest_framework import viewsets,permissions
# Create your views here.


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()
    

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ProductReadSerializer
        else:
            return ProductWriteSerializer
