# Generated by Django 5.1.1 on 2024-10-07 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0014_alter_ordereddrinks_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='John Walker', max_length=50, verbose_name='Drink Name')),
                ('contact', models.CharField(default='+254', max_length=20)),
                ('role', models.CharField(default='Supplier', max_length=50)),
                ('picture', models.ImageField(default='Contact/default.jpg', null=True, upload_to='Contact')),
            ],
        ),
        migrations.AlterField(
            model_name='drinks',
            name='name',
            field=models.CharField(default='', max_length=50, verbose_name='Drink Name'),
        ),
    ]
