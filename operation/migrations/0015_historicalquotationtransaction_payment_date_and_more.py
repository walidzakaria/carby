# Generated by Django 5.1.4 on 2025-01-20 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0014_historicalquotationtransaction_quotationtransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalquotationtransaction',
            name='payment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quotationtransaction',
            name='payment_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
