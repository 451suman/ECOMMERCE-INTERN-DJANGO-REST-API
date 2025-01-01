from django.db import models
from product.models import Product
from django.contrib.auth.models import User

StatusChoice = [
    ('Pending', 'Pending'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusChoice, default='Pending')
    totalAmount = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.status} - {self.totalAmount} - {self.created_on}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)  # Add related_name for reverse lookup
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()

    def __str__(self):
        return f"{self.order.user} - {self.product} - {self.quantity} - {self.unit_price}"


    