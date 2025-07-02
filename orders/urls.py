from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CatererOrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'caterer/orders', CatererOrderViewSet, basename='caterer-orders')

urlpatterns = [
    path('', include(router.urls)),
]