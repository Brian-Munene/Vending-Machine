# Generated by Django 3.2.13 on 2022-05-24 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cointype',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]
