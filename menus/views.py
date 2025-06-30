

from rest_framework import viewsets, permissions
from .models import Menu, MenuItem, Category, CustomizationOption
from .serializers import MenuSerializer, MenuItemSerializer, CategorySerializer, CustomizationOptionSerializer
from .permissions import IsCaterer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsCaterer()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(caterer=self.request.user)

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsCaterer()]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CustomizationOptionViewSet(viewsets.ModelViewSet):
    queryset = CustomizationOption.objects.all()
    serializer_class = CustomizationOptionSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsCaterer()]
        return [permissions.AllowAny()]
