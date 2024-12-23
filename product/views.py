from django.shortcuts import render
from product.models import Product
from product.serializers import  ProductSerializer
from rest_framework import viewsets,permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response 

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



class ProductViewset(APIView):


    def get(self, request, pk = None):
        if pk:
            try:
                product = Product.objects.get(pk=pk)
            except Product.DoesNotExist:
                return Response({"messages":"Product not found" }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            product = Product.objects.all().order_by("-id")
            serializer = ProductSerializer(product, many= True)
            return Response(serializer.data, status= status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)