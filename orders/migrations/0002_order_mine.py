# Generated by Django 3.1.1 on 2021-04-19 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='mine',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='mwene', to='home.shopprofile'),
            preserve_default=False,
        ),
    ]
