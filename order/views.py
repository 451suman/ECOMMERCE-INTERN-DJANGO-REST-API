from rest_framework import viewsets
from rest_framework import permissions
from order.models import Order
from order.serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user = self.request.user).order_by('created_on')
        return queryset