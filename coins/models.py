from django.db import models
import uuid


class CoinType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=200)


class Coins(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    coin_type = models.ForeignKey(CoinType, on_delete=models.PROTECT)
    coin_count = models.IntegerField(default=0, null=False, blank=False)

