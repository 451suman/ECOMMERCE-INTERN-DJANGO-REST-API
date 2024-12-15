from django.contrib.auth.models import Group, User
# from rest_framework import permissions, viewsets
from rest_framework.views import APIView

from authentication.serializers import LoginSerializer
# from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password


class LoginViewSet(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Return specific error if username is incorrect
            return Response({
                "status": "failed",
                "message": "Username is incorrect"
            })
        
        if not check_password(password, user.password):
            # Return specific error if password is incorrect
            return Response({
                "status": "failed",
                "message": "Password is incorrect"
            })

        refresh = RefreshToken.for_user(user)
        return Response ({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            "success": True,
            "message": "Login successfull"
        })
    


        
# username = request.GET.get('username')
#use get when data is requested from url
#http://127.0.0.1:8000/authentication/login/?username="suman