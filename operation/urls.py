from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet, VendorViewSet, QuotationViewSet, StockViewSet


urlpatterns = []

router = DefaultRouter()
router.register('vendor', VendorViewSet, basename='vendor')
router.register('customer', CustomerViewSet, basename='customer')
router.register('quotation', QuotationViewSet, basename='quotation')
router.register('stock', StockViewSet, basename='stock')

urlpatterns += router.urls
