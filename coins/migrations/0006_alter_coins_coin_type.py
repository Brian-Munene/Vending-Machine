# Generated by Django 3.2.13 on 2022-05-25 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0005_auto_20220525_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coins',
            name='coin_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='coins', to='coins.cointype'),
        ),
    ]
