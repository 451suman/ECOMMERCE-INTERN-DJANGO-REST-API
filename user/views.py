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
