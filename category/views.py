from django.shortcuts import render

from category.models import Category
from category.serializers import CategorySerializer
from rest_framework import permissions
from rest_framework import viewsets

# Create your views here.
class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class =CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return (permissions.AllowAny(),)
        return super().get_permissions()

