# Generated by Django 3.1.4 on 2021-01-08 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_transfers_accountnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfers',
            name='accountNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]