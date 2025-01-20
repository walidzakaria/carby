from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet, VendorViewSet, QuotationViewSet


urlpatterns = []

router = DefaultRouter()
router.register('vendor', VendorViewSet, basename='vendor')
router.register('customer', CustomerViewSet, basename='customer')
router.register('quotation', QuotationViewSet, basename='quotation')

urlpatterns += router.urls
