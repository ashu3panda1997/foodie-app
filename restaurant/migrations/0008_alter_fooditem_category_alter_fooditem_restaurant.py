# Generated by Django 4.2.20 on 2025-03-16 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_remove_category_restaurant_alter_fooditem_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fooditems', to='restaurant.category'),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_items', to='restaurant.restaurant'),
        ),
    ]
