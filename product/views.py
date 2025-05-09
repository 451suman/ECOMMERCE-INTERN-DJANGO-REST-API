from django.shortcuts import render
from product.models import Product
from product.serializers import ProductSerializer, ProductReadSerializer
# from product.serializers import ProductWriteSerializer, ProductReadSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import filters
# Create your views here.


# class ProductViewset(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     permission_classes = [permissions.IsAdminUser]

#     def get_permissions(self):
#         if self.action in ['list','retrieve']:
#             return [permissions.AllowAny()]
#         return super().get_permissions()


#     def get_serializer_class(self):
#         if self.action in ["list", "retrieve"]:
#             return ProductReadSerializer
#         else:
#             return ProductWriteSerializer

from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import filters
from .models import Product
from .serializers import ProductReadSerializer, ProductSerializer

class ProductViewset(APIView):
    permission_classes = [IsAdminUser]  # By default, allow only admin users
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_permissions(self):
        # Allow any user to list and retrieve categories
        # Only admin users can perform POST, PUT, DELETE
        if self.request.method in ['GET']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get(self, request, pk=None):
        # If pk is provided, return the specific product
        if pk:
            try:
                product = Product.objects.get(pk=pk)
            except Product.DoesNotExist:
                return Response(
                    {"messages": "Product not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = ProductReadSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Apply search filter manually using the search query
            search_query = request.GET.get('search', None)
            if search_query:
                product = Product.objects.filter(
                    name__icontains=search_query
                ) | Product.objects.filter(description__icontains=search_query)
            else:
                product = Product.objects.all().order_by("-id")
            
            serializer = ProductReadSerializer(product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"message": "Product not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response({"message": "Product Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
