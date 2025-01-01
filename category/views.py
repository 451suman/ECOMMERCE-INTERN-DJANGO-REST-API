from django.shortcuts import render

from category.models import Category
from category.serializers import CategorySerializer
from rest_framework import status

from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
# class CategoryViewset(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class =CategorySerializer
#     permission_classes = [permissions.IsAdminUser]
    
#     def get_permissions(self):
#         if self.action in ['list','retrieve']:
#             return (permissions.AllowAny(),)
#         return super().get_permissions()




class CategoryViewSet(APIView):
    permission_classes = [IsAdminUser]  # By default, allow anyone
    
    def get_permissions(self):
        
        if self.request.method in ['GET']:
            # Only admin users can perform POST, PUT, DELETE
            self.permission_classes = [AllowAny]
        else:
            # Allow any user to list and retrieve categories
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get(self, request, pk=None):
        if pk:
            try:
                category = Category.objects.get(pk=pk)
            except Category.DoesNotExist:
                return Response({"error": "Category Not Found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            categories = Category.objects.all().order_by("-id")
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Only admin users can create categories
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk):
        # Only admin users can update categories
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category Not Found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Update error."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Only admin users can delete categories
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        category.delete()
        return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)

    def patch(Self,request, pk):
        try :
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CategorySerializer(category, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "partial update  Failed"}, status=status.HTTP_400_BAD_REQUEST)
