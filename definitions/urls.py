from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, DescriptionViewSet, UnitTypeViewSet, ConditionViewSet, BankAccountViewSet, CountryViewSet


urlpatterns = []

router = DefaultRouter()
router.register('product', ProductViewSet, basename='product')
router.register('description', DescriptionViewSet, basename='description')
router.register('unit-type', UnitTypeViewSet, basename='unit-type')
router.register('condition', ConditionViewSet, basename='condition')
router.register('bank-account', BankAccountViewSet, basename='bank-account')
router.register('country', CountryViewSet, basename='country')

urlpatterns += router.urls
