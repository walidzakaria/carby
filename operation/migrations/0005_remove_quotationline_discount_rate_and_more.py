# Generated by Django 5.1.4 on 2024-12-14 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0004_remove_historicalquotation_branch_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotationline',
            name='discount_rate',
        ),
        migrations.RemoveField(
            model_name='quotationline',
            name='tax',
        ),
        migrations.AddField(
            model_name='historicalquotation',
            name='net_amount',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='historicalquotation',
            name='tax',
            field=models.CharField(choices=[('T1', 'Value added tax'), ('T2', 'Table tax (percentage)')], default=0, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalquotation',
            name='tax_amount',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='historicalquotation',
            name='total_amount',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotation',
            name='net_amount',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotation',
            name='tax',
            field=models.CharField(choices=[('T1', 'Value added tax'), ('T2', 'Table tax (percentage)')], default=0, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quotation',
            name='tax_amount',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotation',
            name='total_amount',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='margin',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotationline',
            name='sales_price',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
    ]
