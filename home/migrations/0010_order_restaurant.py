# Generated by Django 4.2.20 on 2025-03-22 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0014_restaurant_owner_restaurant_slug'),
        ('home', '0009_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
    ]
