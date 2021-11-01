from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.ShopListView.as_view(),name="shops_index"),
    path('<slug:shop_name>/',views.ShopDetailView.as_view(),name="shops_detail"),
]
