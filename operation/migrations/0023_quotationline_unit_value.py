# Generated by Django 5.1.4 on 2025-01-24 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0022_historicalquotation_total_cost_quotation_total_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationline',
            name='unit_value',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
    ]
