from django.contrib import admin
from .models import Customer, Quotation, QuotationLine, Vendor


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('governate', 'region_city', 'type', 'customer_id', 'name', )
    list_filter = ('type', )
    search_fields = ('customer_id', 'name', )
    readonly_fields = ('creation_date', 'modified_date', 'created_by', 'updated_by', )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)


class QuotationLineTabular(admin.TabularInline):
    model = QuotationLine
    extra = 1


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_time_issued', 'internal_id', )
    search_fields = ('customer__name', 'internal_id', )
    inlines = [QuotationLineTabular]
    readonly_fields = ('creation_date', 'modified_date', 'created_by', 'updated_by', )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'instapay', 'bank_account', )
    search_fields = ('name', 'phone', )
    readonly_fields = ('creation_date', 'modified_date', 'created_by', 'updated_by', )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)
