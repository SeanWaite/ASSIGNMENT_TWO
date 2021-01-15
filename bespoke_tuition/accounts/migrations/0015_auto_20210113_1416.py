# Generated by Django 3.1.4 on 2021-01-13 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_invoices_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='invoice_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_no', to='accounts.invoices'),
        ),
    ]
