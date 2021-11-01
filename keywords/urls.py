from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.KeywordListView.as_view(),name="keywords_index"),
]
