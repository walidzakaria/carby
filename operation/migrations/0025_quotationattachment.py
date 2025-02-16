# Generated by Django 5.1.4 on 2025-02-15 15:30

import django.db.models.deletion
import operation.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0024_quotationline_country_quotationline_margin_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuotationAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='quotation/attachment/', validators=[operation.validators.validate_pdf])),
                ('file_type', models.CharField(choices=[('CONDITIONS', 'كراسة شروط'), ('SUPPLY_ORDER', 'امر توريد'), ('PAYMENT_ORDER', 'امر دفع'), ('OTHER', 'اخرى')], default='OTHER', max_length=15)),
                ('file_name', models.CharField(max_length=50)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operation.quotation')),
            ],
            options={
                'verbose_name': 'Quotation Attachment',
                'verbose_name_plural': 'Quotation Attachments',
            },
        ),
    ]
