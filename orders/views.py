from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.user != request.user:
            return Response({'error': 'Unauthorized'}, status=400)
        order.status != 'accepted'
        order.save()
        return Response({'message': 'Order confirmed', "status": order.status})


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from users.permissions import IsCaterer

class CatererOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsCaterer]

    def list(self, request):
        orders = Order.objects.filter(items__menu_item__menu__caterer=request.user.caterer).distinct()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk, items__menu_item__menu__caterer=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or not for your menu'}, status=404)
        
        new_status = request.data.get('status')
        if new_status not in dict(Order._meta.get_field('status').choices):
            return Response({'error': 'Invalid status'}, status=400)
        
        order.status = new_status
        order.save()
        return Response({"message": f"Order status updated to {new_status}"})
    
from django.http import FileResponse
from .utils import generate_invoice_pdf

@action(detail=True, methods=['get'])
def invoice(self, request, pk=None):
    order = self.get_object()
    if order.user != request.user and not request.user.is_staff:
        return Response({"error": "Unauthorized"}, status=403)

    buffer = generate_invoice_pdf(order)
    return FileResponse(buffer, as_attachment=True, filename=f"invoice_{order.id}.pdf")
