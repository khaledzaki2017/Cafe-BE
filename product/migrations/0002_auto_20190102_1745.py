# Generated by Django 2.1.4 on 2019-01-02 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outlet', '0006_auto_20190102_1745'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comboproduct',
            name='combo_product',
        ),
        migrations.RemoveField(
            model_name='comboproduct',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='comboproduct',
            name='instate_tax',
        ),
        migrations.RemoveField(
            model_name='comboproduct',
            name='interstate_tax',
        ),
        migrations.RemoveField(
            model_name='comboproduct',
            name='uom',
        ),
        migrations.DeleteModel(
            name='ComboProduct',
        ),
    ]
