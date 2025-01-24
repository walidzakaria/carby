from django.contrib import admin
from .models import Customer, Quotation, QuotationLine, Vendor, QuotationTransaction, Stock


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('governate', 'region_city', 'type', 'customer_id', 'name', )
    list_filter = ('type', 'is_active', )
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
    list_display = ('id', 'customer', 'date_time_issued', )
    search_fields = ('customer__name', )
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
    list_filter = ('is_active', )
    readonly_fields = ('creation_date', 'modified_date', 'created_by', 'updated_by', )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'description', 'quantity', 'unit_type', 'unit_value', 'total_value', )
    search_fields = ('product__name', 'description__name', )
    readonly_fields = ('creation_date', 'modified_date', 'created_by', 'updated_by', )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user


@admin.register(QuotationTransaction)
class QuotationTransactionAdmin(admin.ModelAdmin):
    list_display = ('quotation', 'cash_type', 'amount', 'transaction_date', 'paid', 'payment_date', )
    list_filter = ('paid', 'cash_type', )
    search_fields = ('quotation__customer__name', 'quotation__customer__customer_id', 'quotation__customer__phone', )
    readonly_fields = ('creation_date', 'modified_date', 'created_by', 'updated_by', )
    autocomplete_fields = ('quotation', 'cash_type', )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)
