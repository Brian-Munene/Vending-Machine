# Generated by Django 3.2.13 on 2022-05-24 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0003_productpurchase_purchasecoins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cointype',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]