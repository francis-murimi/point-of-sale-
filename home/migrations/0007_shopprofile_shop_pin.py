# Generated by Django 3.1.1 on 2021-05-05 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_shopprofile_shop_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopprofile',
            name='shop_pin',
            field=models.CharField(default='12345', help_text='Shop administration pin', max_length=10),
        ),
    ]
