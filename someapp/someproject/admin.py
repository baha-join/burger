from django.contrib import admin
from .models import User, Category, Dish, MenuDay, MenuItem, PickupSlot, Order, OrderItem

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(MenuDay)
admin.site.register(MenuItem)
admin.site.register(PickupSlot)
admin.site.register(Order)
admin.site.register(OrderItem)