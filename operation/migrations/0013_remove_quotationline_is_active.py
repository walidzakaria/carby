# Generated by Django 5.1.4 on 2025-01-19 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0012_rename_actual_quantity_quotationline_quotation_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotationline',
            name='is_active',
        ),
    ]
