from rest_framework import serializers
from .models import Category, Menu, MenuItem, CustomizationOption

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CustomizationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomizationOption
        fields = [
            'id', 'label', 'extra_price',
            'spice_level', 'allergens', 'dietary_tag'
        ]

class MenuItemSerializer(serializers.ModelSerializer):
    customizations = CustomizationOptionSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id', 'menu', 'name', 'description',
            'price', 'category', 'customizations'
        ]


class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)
    caterer = serializers.StringRelatedField(read_only=True)  # show email/full name

    class Meta:
        model = Menu
        fields = ['id', 'caterer', 'title', 'description', 'items']
