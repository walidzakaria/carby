from django.urls import path

from .views import (
  SupplyOrdersView, QuotationOrdersView
)

urlpatterns = [
    path('supply-orders/', SupplyOrdersView.as_view(), name='supply-orders'),
    path('quotation-orders/', QuotationOrdersView.as_view(), name='quotation-orders'),
]
