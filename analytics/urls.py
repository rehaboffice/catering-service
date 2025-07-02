from django.urls import path
from .views import (
    TotalOrdersView, TotalSalesView, TotalUsersView,
    TopItemsView, OrdersLast7DaysView
)

urlpatterns = [
    path('orders/total/', TotalOrdersView.as_view()),
    path('sales/total/', TotalSalesView.as_view()),
    path('users/total/', TotalUsersView.as_view()),
    path('top-items/', TopItemsView.as_view()),
    path('orders/last-7-days/', OrdersLast7DaysView.as_view()),
]
