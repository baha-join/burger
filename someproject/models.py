from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MenuDay(models.Model):
    date = models.DateField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"Меню на {self.date}"

class MenuItem(models.Model):
    menu_day = models.ForeignKey(MenuDay, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    portions_left = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.dish.name} ({self.menu_day.date})"

class PickupSlot(models.Model):
    date = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    capacity = models.IntegerField(default=10)
    booked_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} {self.time_from}-{self.time_to}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('ready', 'Готов к выдаче'),
        ('completed', 'Выдан'),
        ('cancelled', 'Отменен'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(PickupSlot, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ №{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.dish.name} x{self.quantity}"