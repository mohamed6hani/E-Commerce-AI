from django.urls import path
from . import views

urlpatterns = [
    path('price/', views.dynamic_price),
]