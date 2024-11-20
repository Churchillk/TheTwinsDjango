# Generated by Django 5.1.1 on 2024-11-08 16:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreDrinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, verbose_name='Drink Name')),
                ('wholesale', models.IntegerField(null=True)),
                ('cost', models.IntegerField(default=100)),
                ('opening_stock', models.IntegerField(default=0)),
                ('added_stock', models.IntegerField(default=0)),
                ('sold_stock', models.IntegerField(default=0)),
                ('closing_stock', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StoreExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense', models.CharField(default='', max_length=100)),
                ('price', models.IntegerField(default=100)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StoreOrderedDrinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(blank=True, max_length=20, unique=True)),
                ('product_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_mode', models.CharField(choices=[('M-pesa', 'M-pesa'), ('Cash', 'Cash')], max_length=50)),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name='DateTime Ordered')),
                ('order_status', models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')], max_length=10)),
                ('drink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_drinks', to='TwinsAdminUsers.storedrinks')),
            ],
        ),
        migrations.CreateModel(
            name='StoreSoldDrinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Debt', 'Debt')], default='paid', max_length=10)),
                ('total', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('payment_mode', models.CharField(choices=[('Till', 'Till'), ('Cash', 'Cash'), ('Debt', 'Debt')], max_length=50, null=True)),
                ('customer', models.CharField(default='', max_length=50)),
                ('customer_contact', models.CharField(default='+254', max_length=20)),
                ('drink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sold_drinks', to='TwinsAdminUsers.storedrinks')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]