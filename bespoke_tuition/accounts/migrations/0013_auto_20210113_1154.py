# Generated by Django 3.1.4 on 2021-01-13 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20210113_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='invoice_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
