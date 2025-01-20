from django.urls import path

from .views import (
  SupplyOrdersView,
)

urlpatterns = [
    path('supply-orders/', SupplyOrdersView.as_view(), name='supply-orders'),
]
