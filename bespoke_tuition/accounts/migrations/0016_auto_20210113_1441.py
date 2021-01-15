# Generated by Django 3.1.4 on 2021-01-13 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210113_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Draft'), ('ISSUED', 'Issued'), ('UNPAID', 'Unpaid'), ('PART_PAID', 'Part paid'), ('PAID', 'Paid')], default=1, max_length=20),
        ),
    ]
