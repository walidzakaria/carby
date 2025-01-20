# Generated by Django 5.1.4 on 2025-01-11 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definitions', '0001_initial'),
        ('operation', '0006_quotationline_total_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationline',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='definitions.product'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quotationline',
            name='description',
            field=models.CharField(max_length=150),
        ),
    ]
