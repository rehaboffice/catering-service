from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Sum, Count
from orders.models import Order, OrderItem
from users.models import User
from menus.models import MenuItem
from datetime import timedelta
from django.utils.timezone import now

class TotalOrdersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_orders = Order.objects.count()
        return Response({'total_orders': total_orders})
    
class TotalSalesView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_sales = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        return Response({"total_sales": total_sales})
    
class TotalUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        return Response({"total_users": total_users})

class TopItemsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        top_items = (OrderItem.objects
                     .values('menu_item__name')
                     .annotate(total_sold=Sum('quantity'))
                     .order_by('-total_sold')[:5])
        return Response({"top_items": top_items})

class OrdersLast7DaysView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        today = now().date()
        data = []
        for i in range(7):
            day = today - timedelta(days=i)
            count = Order.objects.filter(created_at__date=day).count()
            data.append({"date": str(day), "count": count})
        return Response({"orders_last_7_days": list(reversed(data))})