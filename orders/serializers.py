from rest_framework import serializers
from .models import Order, OrderItem
from menus.models import MenuItem
from django.core.mail import send_mail
from django.db import transaction
from notifications.utils import create_notification


import uuid

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'price']
        read_only_fields = ['price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'total_price', 'items']
        read_only_fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        with transaction.atomic():
            order = Order.objects.create(user=user, **validated_data)
            total = 0

        for item_data in items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']

            if menu_item.stock_quantity < quantity:
                raise serializers.ValidationError(
                    f"'{menu_item.name}' does not have enough stock (only {menu_item.stock_quantity} left)."
                )

            price = menu_item.price * quantity
            OrderItem.objects.create(
                order=order, 
                menu_item=menu_item, 
                quantity=quantity, 
                price=price
            )

            menu_item.stock_quantity -= quantity
            menu_item.save()

            total += price
            caterer = menu_item.menu.caterer
            send_mail(
                subject='New Order Received',
                message=f"You have a new order for {menu_item.name} (x{quantity}).",
                from_email=None,
                recipient_list=[caterer.email],
            )

        order.total_price = total
        order.invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        order.save()
        send_mail(
            subject='Order Received',
            message=f'Thank you for your order #{order.id}. Total: ${order.total_price}.',
            from_email=None,
            recipient_list=[user.email],
        )

        create_notification(user, f"Your order #{order.id} has been placed successfully.")

        # Notify caterers
        for item_data in items_data:
            caterer = item_data['menu_item'].menu.caterer
            create_notification(caterer, f"New order received for: {item_data['menu_item'].name}")
        return order