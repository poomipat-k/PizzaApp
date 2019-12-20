# Generated by Django 3.0 on 2019-12-15 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DinnerPlatterMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('size', models.CharField(max_length=10)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PastaMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PizzaMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=32)),
                ('size', models.CharField(max_length=10)),
                ('topping_option', models.IntegerField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SaladMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SubMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('size', models.CharField(max_length=10)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SubsAddOn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='DinnerPlatter',
            fields=[
                ('dinnerplattermenu_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.DinnerPlatterMenu')),
            ],
            bases=('orders.dinnerplattermenu',),
        ),
        migrations.CreateModel(
            name='Pasta',
            fields=[
                ('pastamenu_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.PastaMenu')),
            ],
            bases=('orders.pastamenu',),
        ),
        migrations.CreateModel(
            name='Salad',
            fields=[
                ('saladmenu_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.SaladMenu')),
            ],
            bases=('orders.saladmenu',),
        ),
        migrations.CreateModel(
            name='Sub',
            fields=[
                ('submenu_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.SubMenu')),
                ('add_on', models.ManyToManyField(blank=True, related_name='on_sub', to='orders.SubsAddOn')),
            ],
            bases=('orders.submenu',),
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('pizzamenu_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.PizzaMenu')),
                ('toppings', models.ManyToManyField(blank=True, related_name='on_pizza', to='orders.Topping')),
            ],
            bases=('orders.pizzamenu',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('pasta', models.ManyToManyField(blank=True, related_name='ordered', to='orders.Pasta')),
                ('pizza', models.ManyToManyField(blank=True, related_name='ordered', to='orders.Pizza')),
                ('platter', models.ManyToManyField(blank=True, related_name='ordered', to='orders.DinnerPlatter')),
                ('salad', models.ManyToManyField(blank=True, related_name='ordered', to='orders.Salad')),
                ('sub', models.ManyToManyField(blank=True, related_name='ordered', to='orders.Sub')),
            ],
        ),
    ]
