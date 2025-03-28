# Generated by Django 5.1.4 on 2025-01-23 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0020_remove_quotationline_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalquotation',
            name='profit_b',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='historicalquotation',
            name='profit_c',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='profit_b',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='profit_c',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True),
        ),
    ]
