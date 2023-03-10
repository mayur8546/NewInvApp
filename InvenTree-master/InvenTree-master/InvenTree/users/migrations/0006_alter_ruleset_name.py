# Generated by Django 3.2.16 on 2023-02-16 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_owner_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ruleset',
            name='name',
            field=models.CharField(choices=[('admin', 'Admin'), ('part_category', 'Part Categories'), ('part', 'Parts'), ('stocktake', 'Stocktake'), ('stock_location', 'Stock Locations'), ('stock', 'Stock Items'), ('build', 'Build Orders'), ('purchase_order', 'Purchase Orders'), ('sales_order', 'Sales Orders')], help_text='Permission set', max_length=50),
        ),
    ]
