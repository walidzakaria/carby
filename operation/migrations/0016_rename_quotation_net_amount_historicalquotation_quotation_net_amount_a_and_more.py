# Generated by Django 5.1.4 on 2025-01-22 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0015_historicalquotationtransaction_payment_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalquotation',
            old_name='quotation_net_amount',
            new_name='quotation_net_amount_a',
        ),
        migrations.RenameField(
            model_name='historicalquotation',
            old_name='quotation_total_amount',
            new_name='quotation_net_amount_b',
        ),
        migrations.RenameField(
            model_name='quotation',
            old_name='quotation_net_amount',
            new_name='quotation_net_amount_a',
        ),
        migrations.RenameField(
            model_name='quotation',
            old_name='quotation_total_amount',
            new_name='quotation_net_amount_b',
        ),
        migrations.AddField(
            model_name='historicalquotation',
            name='po_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='historicalquotation',
            name='quotation_net_amount_c',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='historicalquotation',
            name='quotation_total_amount_a',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='historicalquotation',
            name='quotation_total_amount_b',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='historicalquotation',
            name='quotation_total_amount_c',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotation',
            name='po_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='quotation_net_amount_c',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotation',
            name='quotation_total_amount_a',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotation',
            name='quotation_total_amount_b',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='quotation',
            name='quotation_total_amount_c',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=15),
        ),
    ]
