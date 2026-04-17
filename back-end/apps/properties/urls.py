from django.urls import path
from . import views

urlpatterns = [
    path("search",      views.PropertySearchView.as_view(), name="properties-search"),
    path("<uuid:pk>",   views.PropertyDetailView.as_view(), name="properties-detail"),
]
