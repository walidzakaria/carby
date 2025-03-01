# Generated by Django 5.1.4 on 2025-01-11 22:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definitions', '0002_alter_description_product'),
        ('operation', '0007_quotationline_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationline',
            name='description',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='definitions.description'),
        ),
    ]
