# Generated by Django 5.1.1 on 2024-10-06 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_solddrinks_customer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='solddrinks',
            options={'ordering': ['date']},
        ),
        migrations.AlterField(
            model_name='solddrinks',
            name='status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Debt', 'Debt')], default='paid', max_length=10),
        ),
    ]
