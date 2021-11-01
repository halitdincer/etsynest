from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.ListingListView.as_view(),name="listings_index"),
    path('<int:listing_id>/',views.ListingDetailView.as_view(),name="listings_detail"),
]
