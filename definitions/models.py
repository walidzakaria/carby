from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Product(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )


class Description(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='descriptions')
    name = models.CharField(max_length=350)
    
    def __str__(self):
        return self.name


class UnitType(models.Model):
    code = models.CharField(max_length=3, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ('code', )


class Condition(models.Model):
    name = models.CharField(max_length=100, unique=True)
    conditions = models.TextField(max_length=2000, blank=True, null=True)
    
    def __str__(self):
        return self.name


class BankAccount(models.Model):
    account_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    
    
    def __str__(self):
        return self.account_name
    
    class Meta:
        ordering = ('account_name', )


class CashType(models.Model):
    
    class CashCategoryType(models.TextChoices):
        REVENUE = 'Revenue', _('Revenue')
        EXPENSE = 'Expense', _('Expense')
        
    class CashTypeType(models.TextChoices):
        CASH = 'Cash', _('Cash')
        CREDIT = 'Credit', _('Credit')
    
    category = models.CharField(max_length=10, choices=CashCategoryType.choices, default=CashCategoryType.REVENUE)
    type = models.CharField(max_length=6, choices=CashTypeType.choices, default=CashTypeType.CASH)
    
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.description


class Country(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Countries'
    