from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_products),
    path('create/', views.create_product),
]