# Generated by Django 4.2.20 on 2025-03-16 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_fooditem_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='restaurant',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
    ]
