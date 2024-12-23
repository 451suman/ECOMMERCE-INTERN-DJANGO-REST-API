from rest_framework import viewsets, status
from rest_framework import permissions
from order.models import Order
from order.serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(user = self.request.user).order_by('created_on')
#         return queryset

class OrderViewSet(APIView):

    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.request.method in ['post']:
            self.permissions = [permissions.IsAuthenticated]
        else:
            self.permissions = [permissions.IsAdminUser]
        return super().get_permissions()

    def get(self, request, pk=None):
        if pk:
            try:
                order = Order.objects.get(pk=pk)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            order = Order.objects.all().order_by("-id")
            serializer = OrderSerializer(order, many =True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

