# Generated by Django 3.0.7 on 2020-09-22 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demoVCImanage', '0004_auto_20200908_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvci',
            name='returnDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vci',
            name='returnDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
