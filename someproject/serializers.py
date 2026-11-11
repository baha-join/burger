from rest_framework import serializers
from .models import MenuItem, Order, OrderItem, PickupSlot, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class MenuItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='dish.name')
    description = serializers.CharField(source='dish.description')
    price = serializers.DecimalField(source='dish.price', max_digits=10, decimal_places=2)
    image = serializers.ImageField(source='dish.image', read_only=True)
    category = CategorySerializer(source='dish.category')
    calories = serializers.IntegerField(source='dish.calories', read_only=True)
    proteins = serializers.DecimalField(source='dish.proteins', max_digits=5, decimal_places=2, read_only=True)
    fats = serializers.DecimalField(source='dish.fats', max_digits=5, decimal_places=2, read_only=True)
    carbs = serializers.DecimalField(source='dish.carbs', max_digits=5, decimal_places=2, read_only=True)
    weight_g = serializers.IntegerField(source='dish.weight_g', read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'portions_left', 'image', 'category', 'calories', 'proteins', 'fats', 'carbs', 'weight_g']

class PickupSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickupSlot
        fields = ['id', 'time_from', 'time_to']

class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='menu_item.dish.name')
    price = serializers.DecimalField(source='menu_item.dish.price', max_digits=10, decimal_places=2)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    slot = PickupSlotSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'username', 'status', 'status_display', 'total_amount', 'created_at', 'slot', 'items']
