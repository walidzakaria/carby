# Generated by Django 5.1.4 on 2025-01-04 14:20

import django.db.models.deletion
import django.utils.timezone
import operation.validators
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('definitions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('governate', models.CharField(max_length=50)),
                ('region_city', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=150)),
                ('building_number', models.CharField(max_length=20)),
                ('additional_information', models.TextField(blank=True, max_length=200, null=True)),
                ('type', models.CharField(choices=[('P', 'Person'), ('B', 'Business'), ('F', 'Foreigner')], default='B', max_length=1)),
                ('customer_id', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='customer_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='customer_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalCustomer',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('governate', models.CharField(max_length=50)),
                ('region_city', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=150)),
                ('building_number', models.CharField(max_length=20)),
                ('additional_information', models.TextField(blank=True, max_length=200, null=True)),
                ('type', models.CharField(choices=[('P', 'Person'), ('B', 'Business'), ('F', 'Foreigner')], default='B', max_length=1)),
                ('customer_id', models.CharField(db_index=True, max_length=20)),
                ('name', models.CharField(max_length=150)),
                ('creation_date', models.DateTimeField(blank=True, editable=False)),
                ('modified_date', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'historical customer',
                'verbose_name_plural': 'historical customers',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalQuotation',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date_time_issued', models.DateTimeField(default=django.utils.timezone.now)),
                ('internal_id', models.CharField(db_index=True, max_length=10)),
                ('purchase_order_description', models.TextField(blank=True, max_length=2000, null=True)),
                ('creation_date', models.DateTimeField(blank=True, editable=False)),
                ('modified_date', models.DateTimeField(blank=True, editable=False)),
                ('supply_order', models.TextField(blank=True, max_length=100, null=True, validators=[operation.validators.validate_pdf])),
                ('conditions', models.TextField(blank=True, max_length=2000, null=True)),
                ('net_amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('tax', models.CharField(choices=[('T1', 'Value added tax'), ('T2', 'Table tax (percentage)')], max_length=2)),
                ('tax_amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('total_amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('customer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='operation.customer')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'historical quotation',
                'verbose_name_plural': 'historical quotations',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalVendor',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=11, null=True)),
                ('instapay', models.CharField(blank=True, max_length=11, null=True)),
                ('bank_account', models.CharField(blank=True, max_length=20, null=True)),
                ('creation_date', models.DateTimeField(blank=True, editable=False)),
                ('modified_date', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'historical vendor',
                'verbose_name_plural': 'historical vendors',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_issued', models.DateTimeField(default=django.utils.timezone.now)),
                ('internal_id', models.CharField(max_length=10, unique=True)),
                ('purchase_order_description', models.TextField(blank=True, max_length=2000, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('supply_order', models.FileField(blank=True, null=True, upload_to='supply_order/', validators=[operation.validators.validate_pdf])),
                ('conditions', models.TextField(blank=True, max_length=2000, null=True)),
                ('net_amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('tax', models.CharField(choices=[('T1', 'Value added tax'), ('T2', 'Table tax (percentage)')], max_length=2)),
                ('tax_amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('total_amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='quotation_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='operation.customer')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='quotation_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=11, null=True)),
                ('instapay', models.CharField(blank=True, max_length=11, null=True)),
                ('bank_account', models.CharField(blank=True, max_length=20, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vendor_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vendor_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
        ),
        migrations.CreateModel(
            name='QuotationLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('unit_value', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('margin', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('sales_price', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('is_active', models.BooleanField(default=True)),
                ('actual_quantity', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('description', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='definitions.description')),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operation.quotation')),
                ('unit_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='definitions.unittype')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='operation.vendor')),
            ],
        ),
    ]
