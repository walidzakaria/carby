# Generated by Django 5.1.4 on 2025-01-22 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definitions', '0007_bankaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
