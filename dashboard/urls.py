# urls.py
from django.urls import path
from .views import (
    UserCountView, VendorCountView, WeeklySalesView, MonthlyIncomeView,
    # CategorySalesView, CategoryDailySalesView, AnnualSalesView
)


urlpatterns = [
    path('user-count/', UserCountView.as_view(), name='user-count'),
    path('vendor-count/', VendorCountView.as_view(), name='vendor-count'),
    path('weekly-sales/', WeeklySalesView.as_view(), name='weekly-sales'),
    path('monthly-income/', MonthlyIncomeView.as_view(), name='monthly-income'),
    # path('category-sales/', CategorySalesView.as_view(), name='category-sales'),
    # path('category-daily-sales/', CategoryDailySalesView.as_view(), name='category-daily-sales'),
    # path('annual-sales/', AnnualSalesView.as_view(), name='annual-sales'),
]
