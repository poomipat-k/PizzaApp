# Generated by Django 3.0 on 2019-12-21 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_pizzaoncart'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PizzaOnCart',
        ),
    ]
