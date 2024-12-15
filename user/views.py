from django.shortcuts import render
from rest_framework.views import APIView
from user.models import Customer
from user.serializers import CustomerSerializer, RegistrationSerializer
from rest_framework import viewsets,permissions
from rest_framework.response import Response
# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            return (permissions.AllowAny(),) 
        elif self.action in ['list','retrieve']:
            return (permissions.IsAdminUser(),)
    
        return super().get_permissions()
    

class RegisterViewset(APIView):
    """
    View to handle user registration and create customer information
    """
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle user registration. Create a user and associated customer record.
        """
        phone = request.data.get('phone')
        address = request.data.get('address')

        # Validate the data using the RegistrationSerializer
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            # Save the user instance
            user = serializer.save()
            return Response({
                'message': 'User registered successfully.',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    # Do not include password
                },
                "success": True
            })

        return Response(serializer.errors, status=400)


    # class RegisterCustomerViewset(APIView):
#     serializer_class = RegistrationSerializer

#     def post(self, request, *args, **kwargs):
#         # Extract phone and address data
#         phone = request.data.get('phone')
#         address = request.data.get('address')

#         # Pass the user data through the serializer
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.save()  # Save the user instance

#             # Create a Customer instance after saving the user
#             Customer.objects.create(user=user, phone=phone, address=address)

#             # Return a response with the user data
#             return Response({'message': 'User created successfully', 'user': serializer.data}, sucess=True)
#         return Response(serializer.errors, status=400)
    

# class dummy(APIView):

#     def post(self, request, *args, **kwargs):

#         phone = request.data.get('phone')
#         address = request.data.get('address')

#         username= request.data.get('username')
#         email = request.data.get('email')
#         password = request.data.get('password')

#         user = User.objects.create_user(username=username, email=email, password=password)

#         Customer.objects.create(user=user, phone=phone, address=address)

#         return Response({'message': 'User created successfully'})
