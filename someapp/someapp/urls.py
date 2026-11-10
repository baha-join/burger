from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from someproject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/menu/', views.api_menu),
    path('api/login/', views.api_login),
    path('api/logout/', views.api_logout),
    path('api/cart/', views.api_cart),
    path('api/cart/add/', views.api_cart_add),
    path('api/cart/clear/', views.api_cart_clear),
    path('api/slots/', views.api_slots),
    path('api/orders/create/', views.api_create_order),
    path('api/orders/my/', views.api_my_orders),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ВНИМАНИЕ: мы дописываем маршрут прямо в конец файла.
# Если сервер упадет с ошибкой синтаксиса, замените urls.py полностью.
urlpatterns += [
    path('api/me/', views.api_me),
]
