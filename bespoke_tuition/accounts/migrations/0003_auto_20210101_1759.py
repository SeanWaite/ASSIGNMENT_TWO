# Generated by Django 3.1.4 on 2021-01-01 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210101_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='date_inserted',
            field=models.DateTimeField(verbose_name='Date Added'),
        ),
    ]
