# Generated by Django 3.2.13 on 2022-05-28 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='public_id',
            new_name='id',
        ),
    ]