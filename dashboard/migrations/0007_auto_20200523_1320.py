# Generated by Django 3.0.6 on 2020-05-23 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20200522_1458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fooditem',
            name='allergens',
        ),
        migrations.RemoveField(
            model_name='fooditem',
            name='cholesterol_100g',
        ),
        migrations.RemoveField(
            model_name='fooditem',
            name='ingredients_text',
        ),
    ]
