from django.db import models
from category.models import Category
# Create your models here.



class Product(models.Model):
    name = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) 
    description = models.TextField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/product_images/', null=True, blank=True)

    def __str__(self):
        return self.name
    


