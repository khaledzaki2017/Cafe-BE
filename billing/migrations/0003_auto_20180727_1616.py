# Generated by Django 2.0.7 on 2018-07-27 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0002_billitem_item'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingheader',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='billingheader',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.Store'),
        ),
    ]
