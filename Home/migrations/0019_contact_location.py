# Generated by Django 5.1.1 on 2024-10-07 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0018_alter_contact_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='location',
            field=models.CharField(default='Nairobi', max_length=50),
        ),
    ]