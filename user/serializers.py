from django.contrib.auth.models import User
from rest_framework import serializers

from user.models import Customer
from rest_framework import permissions


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CustomerSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address', "created_on", "update_on"]


class RegistrationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=10, required=True)
    address = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone', 'address') 
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Pop the phone and address fields so that they can be passed later to the Customer model
        phone = validated_data.pop('phone')
        address = validated_data.pop('address')
        
        # Create the user
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # After saving the user, create the Customer object
        Customer.objects.create(user=user, phone=phone, address=address)

        return user
    
    def validate_phone(self, value):
        
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError("Mobile number must be exactly 10 digits and contain only numbers.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    # The clean_phone method is not used in the ModelSerializer like it would be in a Form. 
    # Instead, you should use the validate_<field_name> method in ModelSerializer to add custom validation.