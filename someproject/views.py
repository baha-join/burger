from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db import transaction
from django.db.models import F
from .models import MenuDay, MenuItem, PickupSlot, Order, OrderItem, User
from .serializers import MenuItemSerializer, PickupSlotSerializer, OrderSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def api_menu(request):
    today = timezone.now().date()
    menu_day = MenuDay.objects.filter(date=today, is_published=True).first()
    if not menu_day:
        return Response({'items': []})
    items = MenuItem.objects.filter(menu_day=menu_day, portions_left__gt=0).select_related('dish', 'dish__category')
    return Response({'items': MenuItemSerializer(items, many=True).data})

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
    if user:
        login(request, user)
        return Response({'status': 'ok', 'is_staff': user.is_staff})
    return Response({'detail': 'Неверный логин или пароль'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    logout(request)
    return Response({'status': 'ok'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_me(request):
    return Response({'id': request.user.id, 'username': request.user.username, 'is_staff': request.user.is_staff})

@api_view(['GET'])
@permission_classes([AllowAny])
def api_cart(request):
    cart = request.session.get('cart', {})
    items, total = [], 0
    for item_id, qty in cart.items():
        mi = MenuItem.objects.filter(id=item_id).first()
        if mi:
            subtotal = mi.dish.price * qty
            total += subtotal
            items.append({'id': mi.id, 'name': mi.dish.name, 'price': mi.dish.price, 'quantity': qty, 'subtotal': subtotal})
    return Response({'items': items, 'total': total})

@api_view(['POST'])
@permission_classes([AllowAny])
def api_cart_add(request):
    item_id = str(request.data.get('item_id'))
    cart = request.session.get('cart', {})
    cart[item_id] = cart.get(item_id, 0) + 1
    request.session['cart'] = cart
    return Response({'status': 'ok'})

@api_view(['POST'])
@permission_classes([AllowAny])
def api_cart_clear(request):
    request.session['cart'] = {}
    return Response({'status': 'ok'})

@api_view(['GET'])
@permission_classes([AllowAny])
def api_slots(request):
    slots = PickupSlot.objects.filter(date=timezone.now().date(), booked_count__lt=F('capacity'))
    return Response(PickupSlotSerializer(slots, many=True).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_order(request):
    cart = request.session.get('cart', {})
    if not cart: return Response({'detail': 'Корзина пуста'}, status=400)
    slot = PickupSlot.objects.filter(id=request.data.get('slot_id')).first()
    if not slot: return Response({'detail': 'Слот не найден'}, status=400)
    
    with transaction.atomic():
        order = Order.objects.create(user=request.user, slot=slot, status='new')
        total = 0
        for item_id, qty in cart.items():
            mi = MenuItem.objects.get(id=item_id)
            OrderItem.objects.create(order=order, menu_item=mi, quantity=qty)
            mi.portions_left -= qty
            mi.save()
            total += mi.dish.price * qty
        order.total_amount = total
        order.save()
        slot.booked_count += 1
        slot.save()
    request.session['cart'] = {}
    return Response({'status': 'ok', 'order_id': order.id})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return Response(OrderSerializer(orders, many=True).data)

# --- НОВОЕ ДЛЯ ПЕРСОНАЛА ---
@api_view(['GET'])
@permission_classes([IsAdminUser])
def api_staff_orders(request):
    today = timezone.now().date()
    orders = Order.objects.filter(created_at__date=today).exclude(status__in=['completed', 'cancelled']).order_by('created_at')
    return Response(OrderSerializer(orders, many=True).data)

@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def api_staff_order_status(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    if not order: return Response({'detail': 'Не найден'}, status=404)
    new_status = request.data.get('status')
    if new_status in ['ready', 'completed', 'cancelled']:
        order.status = new_status
        order.save()
        return Response({'status': 'ok'})
    return Response({'detail': 'Неверный статус'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'detail': 'Логин и пароль обязательны'}, status=400)
    if len(password) < 6:
        return Response({'detail': 'Пароль минимум 6 символов'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'detail': 'Пользователь уже существует'}, status=400)
        
    user = User.objects.create_user(username=username, password=password)
    return Response({'status': 'ok', 'message': 'Пользователь создан'})
