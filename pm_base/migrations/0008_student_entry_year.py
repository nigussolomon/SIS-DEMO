# Generated by Django 4.2.2 on 2023-06-14 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pm_base', '0007_alter_paymentinformation_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='entry_year',
            field=models.IntegerField(default=2023),
        ),
    ]
