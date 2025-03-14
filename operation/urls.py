from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
  CustomerViewSet, VendorViewSet, QuotationViewSet, StockViewSet, QuotationAttachmentViewSet,
  QuotationInsuranceViewSet,
)


urlpatterns = []

router = DefaultRouter()
router.register('vendor', VendorViewSet, basename='vendor')
router.register('customer', CustomerViewSet, basename='customer')
router.register('quotation', QuotationViewSet, basename='quotation')
router.register('stock', StockViewSet, basename='stock')
router.register('attachment', QuotationAttachmentViewSet, basename='attachment')
router.register('insurance', QuotationInsuranceViewSet, basename='insurance')

urlpatterns += router.urls
