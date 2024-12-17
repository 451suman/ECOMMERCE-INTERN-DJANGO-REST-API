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
    orderitems = OrderItemSerializer(many=True, required=False)  # Make orderitems optional

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'totalAmount', 'orderitems']
        read_only_fields = ['totalAmount', 'user']

    def create(self, validated_data):
        # Ensure the user is set to the logged-in user if not provided
        user = self.context['request'].user  # Get the user from the request context
        validated_data['user'] = user

        # Proceed with order creation as usual
        orderitems_data = validated_data.pop('orderitems', [])
        order = Order.objects.create(**validated_data)

        # Calculate total amount based on the order items
        total_amount = sum(item['quantity'] * item['unit_price'] for item in orderitems_data)
        order.totalAmount = total_amount
        order.save()

        # Create order items for the order
        for item_data in orderitems_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        # Set the user to the current logged-in user if not provided
        user = self.context['request'].user  # Get the user from the request context
        validated_data['user'] = validated_data.get('user', user)  # Set user only if not in validated_data

        # Update the basic fields of the order
        instance.status = validated_data.get('status', instance.status)
        instance.user = validated_data['user']  # Ensure the user is always the logged-in user

        # Handle 'orderitems' update, if provided
        orderitems_data = validated_data.get('orderitems', None)

        if orderitems_data is not None:
            # Recalculate totalAmount based on the new order items
            total_amount = sum(item['quantity'] * item['unit_price'] for item in orderitems_data)
            instance.totalAmount = total_amount
            instance.save()

            # Delete old order items and create new ones
            instance.orderitems.all().delete()
            for item_data in orderitems_data:
                OrderItem.objects.create(order=instance, **item_data)
        
        # Save the instance if no order items are being updated
        instance.save()

        return instance

    def validate(self, data):
        # Ensure totalAmount is calculated based on orderitems, if provided
        if 'orderitems' in data:
            total_amount = sum(item['quantity'] * item['unit_price'] for item in data['orderitems'])
            data['totalAmount'] = total_amount

        return data
