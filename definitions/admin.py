from django.contrib import admin
from .models import Product, Description, UnitType, Condition, CashType, BankAccount, Country


class DescriptionInline(admin.TabularInline):
    model = Description
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', )
    search_fields = ('code', 'name', )
    inlines = [DescriptionInline, ]
    

@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', )
    search_fields = ('product__code', 'product__name', 'name', )


@admin.register(UnitType)
class UnitTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', )
    search_fields = ('code', 'description', )


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(CashType)
class CashTypeAdmin(admin.ModelAdmin):
    list_display = ('category', 'type', 'description', )
    search_fields = ('category', 'type', 'description', )
    list_filter = ('category', 'type', )


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'bank_name', 'account_number', )
    search_fields = ('account_name', 'bank_name', 'account_number', )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('id', 'name', )
