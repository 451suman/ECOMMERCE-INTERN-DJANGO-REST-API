from rest_framework import viewsets, status
from rest_framework import permissions
from order.models import Order, OrderItem
from order.serializers import (
    OrderItemSerializer,
    OrderReadserializer,
    OrderWriteserializer,
)
from rest_framework.generics import ListAPIView

from rest_framework.views import APIView
from rest_framework.response import Response


class OrderItemViewSet(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk=None):
        if pk:
            try:
                order_item = OrderItem.objects.filter(order=pk)
                serializer = OrderItemSerializer(order_item, many=True)
                return Response(
                    {
                        "message": "order items list of specific id",
                        "status": "success",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            except OrderItem.DoesNotExist:
                return Response({"message": "order item not found"})
        else:
            order_item = OrderItem.objects.all()
            serializer = OrderItemSerializer(order_item, many=True)
            return Response(
                {
                    "mesage": "Get all order items",
                    "status": "success",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )


class OrderViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method.lower() in ["post", "put"]:

            return [permissions.IsAuthenticated()]
        else:
            self.permissions = [permissions.IsAdminUser]
        return super().get_permissions()

    def get(self, request, pk=None):
        if pk:
            try:
                order = Order.objects.get(pk=pk)
                serializer = OrderReadserializer(order)
                return Response(
                    {
                        "message": "Retrieve Order",
                        "status": "Success",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            except Order.DoesNotExist:
                return Response(
                    {
                        "message": "Retrieve Order Failed",
                        "status": "Failed",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            order = Order.objects.all().order_by("-id")
            serializer = OrderReadserializer(order, many=True)
            return Response(
                {
                    "message": "get all Order",
                    "status": "Success",
                    "data": serializer.data,
                }
            )

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = OrderWriteserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "order created succcessfully",
                    "status": "success",
                    "data": serializer.data,
                }
            )
        else:
            return Response(
                {
                    "message": "Order Creation Failed",
                    "status": "Failed",
                    "data": serializer.errors,
                }
            )

    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderWriteserializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Order updated successfully",
                        "status": "success",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "message": "Order updated failed.",
                        "status": "Failed",
                    }
                )
        except Order.DoesNotExist:
            return Response(
                {
                    "message": "Order not found",
                    "status": "Failed",
                }
            )

class GetSelfCustomerOrder(ListAPIView):
    model = Order
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderReadserializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    