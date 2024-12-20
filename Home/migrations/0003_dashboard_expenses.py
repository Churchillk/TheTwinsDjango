# Generated by Django 5.1.1 on 2024-10-04 22:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_solddrinks'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_at_hand', models.IntegerField(default=0, null=True)),
                ('cash_at_bank', models.IntegerField(default=0, null=True)),
                ('expenses', models.IntegerField(default=0, null=True)),
                ('total_sales', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense', models.CharField(default='', max_length=100)),
                ('price', models.IntegerField(default=100)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
