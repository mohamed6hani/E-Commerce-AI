"""
URL configuration for the eCommerce AI project.

Routes the admin interface and includes app‑specific URLs.
"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),
    path('api/users/', include('users.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/ai/', include('ai.urls')),
]