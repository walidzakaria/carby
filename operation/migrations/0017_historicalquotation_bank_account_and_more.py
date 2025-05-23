# Generated by Django 5.1.4 on 2025-01-22 15:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definitions', '0007_bankaccount'),
        ('operation', '0016_rename_quotation_net_amount_historicalquotation_quotation_net_amount_a_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalquotation',
            name='bank_account',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='definitions.bankaccount'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='definitions.bankaccount'),
        ),
    ]
