from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

from .validators import validate_pdf
from definitions.models import Description, UnitType, Product, CashType, BankAccount, Country

# Create your models here.
class Customer(models.Model):
    
    class CustomerType(models.TextChoices):
        PERSON = 'P', _('Person')
        BUSINESS = 'B', _('Business')
        FOREIGNER = 'F', _('Foreigner')
    
    name = models.CharField(max_length=150)
    governate = models.CharField(max_length=50)
    region_city = models.CharField(max_length=50)
    street = models.CharField(max_length=150)
    building_number = models.CharField(max_length=20)
    additional_information = models.TextField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=1, choices=CustomerType.choices, default=CustomerType.BUSINESS)
    customer_id = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='customer_created_by',
                                   verbose_name=_('Created By'), blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='customer_updated_by',
                                   verbose_name=_('Updated By'), blank=True, null=True)
    history = HistoricalRecords()
    
    
    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11, blank=True, null=True)
    instapay = models.CharField(max_length=50, blank=True, null=True)
    bank_account = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='vendor_created_by',
                                   verbose_name=_('Created By'), blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='vendor_updated_by',
                                   verbose_name=_('Updated By'), blank=True, null=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    description = models.ForeignKey(Description, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=15, decimal_places=5)
    unit_type = models.ForeignKey(UnitType, on_delete=models.PROTECT)
    unit_value = models.DecimalField(max_digits=15, decimal_places=5)
    total_value = models.DecimalField(max_digits=15, decimal_places=5)
    
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='stock_created_by',
                                   verbose_name=_('Created By'), blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='stock_updated_by',
                                   verbose_name=_('Updated By'), blank=True, null=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f'{self.product} - {self.quantity}'


class Quotation(models.Model):
    
    class StatusOption(models.TextChoices):
        QUOTATION = 'Quotation', _('Quotation')
        CANCELED = 'Canceled', _('Canceled')
        INVOICE = 'Invoice', _('Invoice')
        CLOSED = 'Closed', _('Closed')
        

    class TaxOption(models.TextChoices):
        T1 = 'T1', _('Value added tax')
        T2 = 'T2', _('Table tax (percentage)')
    
    status = models.CharField(max_length=15, choices=StatusOption.choices, default=StatusOption.QUOTATION,
                              verbose_name=_('Status'))
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    date_time_issued = models.DateTimeField(default=timezone.now)

    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='quotation_created_by',
                                   verbose_name=_('Created By'), blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='quotation_updated_by',
                                   verbose_name=_('Updated By'), blank=True, null=True)
    supply_order = models.FileField(upload_to='supply_order/', validators=[validate_pdf],
                                    blank=True, null=True)
    po_number = models.CharField(max_length=20, blank=True, null=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, blank=True, null=True)
    conditions = models.TextField(max_length=2000, blank=True, null=True)
    tax = models.CharField(max_length=2, choices=TaxOption.choices)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    quotation_net_amount_a = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    quotation_net_amount_b = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    quotation_net_amount_c = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    quotation_total_amount_a = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    quotation_total_amount_b = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    quotation_total_amount_c = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    total_cost = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    net_amount = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    total_amount = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    profit_a = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    profit_b = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    profit_c = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.id}'
    

class QuotationLine(models.Model):
    
    class LabelOption(models.TextChoices):
        A = 'A', _('A')
        B = 'B', _('B')
        C = 'C', _('C')
    
    
    class SourceOption(models.TextChoices):
        VENDOR = 'Vendor', _('Vendor')
        STOCK = 'Stock', _('Stock')
    
    
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='lines')
    source = models.CharField(max_length=10, choices=SourceOption.choices, default=SourceOption.VENDOR)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    description = models.ForeignKey(Description, on_delete=models.PROTECT)
    
    country_a = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='country_a', blank=True, null=True)
    country_b = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='country_b', blank=True, null=True)
    country_c = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='country_c', blank=True, null=True)
    
    unit_value_a = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    unit_value_b = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    unit_value_c = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    
    margin_a = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    margin_b = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    margin_c = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    
    sales_price_a = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    sales_price_b = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    sales_price_c = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    
    quotation_total_value_a = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    quotation_total_value_b = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    quotation_total_value_c = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    
    unit_type = models.ForeignKey(UnitType, on_delete=models.PROTECT)
    quotation_quantity = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    
    label = models.CharField(max_length=1, choices=LabelOption.choices, default=LabelOption.A)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='country', blank=True, null=True)
    unit_value = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    margin = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    sales_price = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    quantity = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    total_value = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)


class QuotationTransaction(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    cash_type = models.ForeignKey(CashType, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=15, decimal_places=5, default=0.00)
    transaction_date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    paid = models.BooleanField(default=False, verbose_name=_('Paid'))
    payment_date = models.DateField(blank=True, null=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='quotation_transaction_created_by',
                                   verbose_name=_('Created By'), blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='quotation_transaction_updated_by',
                                   verbose_name=_('Updated By'), blank=True, null=True)
    
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.id}'
