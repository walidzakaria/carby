# Generated by Django 5.1.4 on 2025-01-22 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definitions', '0008_country'),
        ('operation', '0017_historicalquotation_bank_account_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quotationline',
            old_name='margin',
            new_name='margin_a',
        ),
        migrations.RenameField(
            model_name='quotationline',
            old_name='quotation_total_value',
            new_name='margin_b',
        ),
        migrations.RenameField(
            model_name='quotationline',
            old_name='sales_price',
            new_name='margin_c',
        ),
        migrations.RenameField(
            model_name='quotationline',
            old_name='unit_value',
            new_name='quotation_total_value_a',
        ),
        migrations.AddField(
            model_name='quotationline',
            name='country_a',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='country_a', to='definitions.country'),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='country_b',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='country_b', to='definitions.country'),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='country_c',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='country_c', to='definitions.country'),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='label',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='quotation_total_value_b',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='quotation_total_value_c',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='sales_price_a',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='sales_price_b',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='sales_price_c',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='unit_value_a',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='unit_value_b',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='unit_value_c',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
    ]
