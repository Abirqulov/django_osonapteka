from django.shortcuts import render
from account.models import *
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import *
# Create your views here.
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['items__drug__drug_name']
    ordering_fields = ['created_at']
    queryset = Order.objects.all()

    def get_queryset(self):
        order = Order.objects.filter(user=self.request.user)
        # is_order_paid(order)

        return order


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def add_order(request):
    try:
        address = request.data['address']
        drug = request.data['drug']
        qty = request.data['qty']
        user = User.objects.filter(id=request.user.id).first()
        Order.objects.create(
            user=user,
            address=address
        )
        order = Order.objects.filter(user=user.id).first()
        drug = Drug.objects.filter(id=drug).first()
        OrderItem.objects.create(
                order=order,
                drug=drug,
                qty=qty,
                price=drug.price,
                subtotal=int(qty)*drug.price
            )

        res = {
            'status': 1
        }
        return Response(res)
    except KeyError:
        res = {
            'error_code': 1
        }
        return Response(res)