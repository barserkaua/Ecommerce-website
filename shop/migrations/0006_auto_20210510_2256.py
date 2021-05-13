# Generated by Django 3.1.7 on 2021-05-10 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210510_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='order',
            name='region',
            field=models.CharField(choices=[('рівненська область', 'Рівненська область'), ('волиська область', 'Волинська область'), ('львівська область', 'Львівська область'), ('тернопільська область', 'Тернопільська область')], default='львівська область', max_length=100),
        ),
    ]