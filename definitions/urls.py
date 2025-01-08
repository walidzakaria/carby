from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, DescriptionViewSet, UnitTypeViewSet


urlpatterns = []

router = DefaultRouter()
router.register('product', ProductViewSet, basename='product')
router.register('description', DescriptionViewSet, basename='description')
router.register('unit-type', UnitTypeViewSet, basename='unit-type')

urlpatterns += router.urls
