# Generated by Django 5.1.4 on 2025-01-14 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0009_alter_quotationline_quotation'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalquotation',
            name='profit',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotation',
            name='profit',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
    ]
