# Generated by Django 5.1.1 on 2024-10-07 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0020_messageuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='solddrinks',
            name='customer_contact',
            field=models.CharField(default='+254', max_length=20),
        ),
    ]