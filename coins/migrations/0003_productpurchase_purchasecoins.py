# Generated by Django 3.2.13 on 2022-05-24 19:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_producttype_slug'),
        ('coins', '0002_cointype_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPurchase',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseCoins',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('coin_count', models.IntegerField(default=0)),
                ('coin_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coins.cointype')),
                ('product_purchase', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coins.productpurchase')),
            ],
        ),
    ]