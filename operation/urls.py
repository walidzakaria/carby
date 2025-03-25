from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
  CustomerViewSet, VendorViewSet, QuotationViewSet, StockViewSet, QuotationAttachmentViewSet,
  QuotationInsuranceViewSet,
)

from .eta import eta_get_invoice, eta_set_status, eta_set_uuid, eta_list_invoices, eta_list_invoice_lines

urlpatterns = []

router = DefaultRouter()
router.register('vendor', VendorViewSet, basename='vendor')
router.register('customer', CustomerViewSet, basename='customer')
router.register('quotation', QuotationViewSet, basename='quotation')
router.register('stock', StockViewSet, basename='stock')
router.register('attachment', QuotationAttachmentViewSet, basename='attachment')
router.register('insurance', QuotationInsuranceViewSet, basename='insurance')

urlpatterns += [
    path('eta-get-invoice/<str:pk>/', eta_get_invoice, name='eta-get-invoice'),
    path('eta-set-status/<str:pk>/', eta_set_status, name='eta-set-status'),
    path('eta-set-uuid/<str:pk>/', eta_set_uuid, name='eta-set-uuid'),
    path('eta-list-invoices/', eta_list_invoices, name='eta-list-invoices'),
    path('eta-list-invoice-lines/<str:pk>/', eta_list_invoice_lines, name='eta-list-invoice-lines'),
]

urlpatterns += router.urls
