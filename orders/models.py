from django.db import models

# Create your models here.
from users.models import User
from menus.models import MenuItem

ORDER_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('preparing', 'Preparing'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

PAYMENT_METHOD_CHOICES = [
    ('cash', 'Cash on Delivery'),
    ('online', 'Online Payment'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='cash')
    invoice_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"
    
    @property
    def caterers(self):
        return set(item.menu_item.menu.caterer for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"