# Generated by Django 5.1.4 on 2025-03-17 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definitions', '0009_alter_bankaccount_options_alter_country_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='description',
            name='name',
            field=models.CharField(max_length=350),
        ),
    ]
