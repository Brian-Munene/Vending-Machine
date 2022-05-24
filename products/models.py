from django.db import models
import uuid


class ProductType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=200, unique=True)


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    product_count = models.IntegerField(default=0, null=False, blank=False)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
