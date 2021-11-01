from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.OrderListView.as_view(),name="orders_index"),
    path('<int:order_id>/',views.OrderDetailView.as_view(),name="orders_detail"),
]
