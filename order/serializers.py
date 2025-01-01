from rest_framework import serializers
from order.models import Order, OrderItem

from django.db.models import F, Sum


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "unit_price"]


class OrderReadserializer(serializers.ModelSerializer):
    totalAmount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "user", "status", "totalAmount", "created_on", "update_on"]

    def get_totalAmount(self, obj):
        order_items = obj.orderitems.all()  # getting all order items
        # F() is a special class used to refer to the value of a model field in a query expression. It allows you to perform operations
        # directly on database fields without needing to retrieve the values into Python memory first.
        total_amount = order_items.aggregate(
            total_amount=Sum(F("unit_price") * F("quantity"))
        )["total_amount"]
        return total_amount


class OrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price"]


class OrderWriteserializer(serializers.ModelSerializer):
    orderitems = OrderItemWriteSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "user",
            "status",
            "totalAmount",
            "orderitems",
        ]

    def create(self, validated_data):
        orderitems_data = validated_data.pop("orderitems")

        total_amount = 0
        for item in orderitems_data:
            total_amount += item["quantity"] * item["unit_price"]

        validated_data["totalAmount"] = total_amount

        order = Order.objects.create(**validated_data)

        for orderitem_data in orderitems_data:
            OrderItem.objects.create(order=order, **orderitem_data)
        return order

    def update(self, instance, validated_data):
        status = validated_data.get("status", instance.status)
        instance.status = status
        instance.save()
        return instance
