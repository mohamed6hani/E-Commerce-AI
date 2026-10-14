from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_orders),
    path('create/', views.create_order),
]