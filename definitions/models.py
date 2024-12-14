from django.db import models

# Create your models here.
class Product(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )


class Description(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    
    def __str__(self):
        return self.description


class UnitType(models.Model):
    code = models.CharField(max_length=3, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description
