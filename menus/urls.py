from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, MenuItemViewSet, CategoryViewSet, CustomizationOptionViewSet

router = DefaultRouter()
router.register(r'menus', MenuViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'customizations', CustomizationOptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
