# Generated by Django 5.1.4 on 2025-02-15 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0025_quotationattachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalquotation',
            name='supply_order',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='supply_order',
        ),
    ]
