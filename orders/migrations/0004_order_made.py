# Generated by Django 3.1.1 on 2021-04-20 12:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_orderitem_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='made',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
