# Generated by Django 3.1.1 on 2021-04-23 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_made'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]