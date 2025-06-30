from django.db import models

# Create your models here.
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Menu(models.Model):
    caterer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'caterer'})
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
SPICE_LEVEL_CHOICES = [
    ('none', 'None'),
    ('mild', 'Mild'),
    ('medium', 'Medium'),
    ('hot', 'Hot'),
]

ALLERGEN_CHOICES = [
    ('nuts', 'Nuts'),
    ('dairy', 'Dairy'),
    ('gluten', 'Gluten'),
    ('soy', 'Soy'),
    ('shellfish', 'Shellfish'),
    ('egg', 'Egg'),
    ('peanut', 'Peanut'),
]

DIETARY_CHOICES = [
    ('vegan', 'Vegan'),
    ('vegetarian', 'Vegetarian'),
    ('gluten_free', 'Gluten Free'),
    ('lactose_free', 'Lactose Free'),
    ('halal', 'Halal'),
    ('kosher', 'Kosher'),
]
    
class CustomizationOption(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='customizations')
    label = models.CharField(max_length=100)
    extra_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    spice_level = models.CharField(max_length=10, choices=SPICE_LEVEL_CHOICES, blank=True, null=True)
    allergens = models.CharField(max_length=100, choices=ALLERGEN_CHOICES, blank=True, null=True)
    dietary_tag = models.CharField(max_length=20, choices=DIETARY_CHOICES, blank=True, null=True)

    def __str__(self):
        parts = [self.label]
        if self.spice_level:
            parts.append(f"Spice: {self.get_spice_level_display()}")
        if self.dietary_tag:
            parts.append(f"Diet: {self.get_dietary_tag_display()}")
        if self.allergens:
            parts.append(f"Allergen: {self.get_allergens_display()}")
        if self.extra_price:
            parts.append(f"+{self.extra_price}")
        return " | ".join(parts)