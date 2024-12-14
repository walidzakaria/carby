from django.contrib import admin
from .models import Product, Description, UnitType

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', )
    search_fields = ('code', 'name', )
    

@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('product', 'description', )
    search_fields = ('product__code', 'product__name', 'description', )


@admin.register(UnitType)
class UnitTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', )
    search_fields = ('code', 'description', )
