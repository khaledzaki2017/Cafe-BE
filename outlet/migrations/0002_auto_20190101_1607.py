# Generated by Django 2.1.4 on 2019-01-01 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('outlet', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='outletproduct',
            unique_together={('outlet', 'product')},
        ),
    ]
