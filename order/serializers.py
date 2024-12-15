from rest_framework import serializers
from order.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem  # Fixed model name to `OrderItem`
        fields = ['id','product', 'quantity', 'unit_price']

    def validate_quantity(self, value):
        # Ensure that quantity is greater than 0
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        return value

class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True)  # A list of items in the order

    class Meta:
        model = Order
        fields = ['id','user', 'status', 'totalAmount', 'orderitems']
        read_only_fields = ['totalAmount']  # Ensure totalAmount is read-only in the API

    def create(self, validated_data):
        # Extract order items from validated data
        orderitems_data = validated_data.pop('orderitems')

        # Create the Order instance without totalAmount (it will be set programmatically)
        order = Order.objects.create(**validated_data)

        # Calculate total amount based on order items
        total_amount = sum(item['quantity'] * item['unit_price'] for item in orderitems_data)
        
        # Update the order's totalAmount field after creation
        order.totalAmount = total_amount
        order.save()

        # Create OrderItem instances for each item in the order
        for item_data in orderitems_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def validate(self, data):
        # Calculate total amount before validating
        total_amount = sum(item['quantity'] * item['unit_price'] for item in data['orderitems'])
        
        # Add the calculated totalAmount to validated data
        data['totalAmount'] = total_amount

        return data
