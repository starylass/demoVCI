# Generated by Django 3.0.7 on 2020-09-07 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demoVCImanage', '0002_auto_20200822_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsalespersondistributor',
            name='idSalesPersonDistributor',
            field=models.IntegerField(blank=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='salespersondistributor',
            name='idSalesPersonDistributor',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
