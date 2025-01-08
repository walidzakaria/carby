from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet, VendorViewSet


urlpatterns = []

router = DefaultRouter()
router.register('vendor', VendorViewSet, basename='vendor')
router.register('customer', CustomerViewSet, basename='customer')

urlpatterns += router.urls
