from django.urls import path
from rest_framework import routers
from .views import ProductTypeViewset, create_product, get_products, get_single_product, update_product, get_product_by_type

router = routers.DefaultRouter()
router.register(r'product/type', ProductTypeViewset, basename='product_type')

urlpatterns = [
    path('create/product', create_product, name='create_product'),
    path('products', get_products, name='products'),
    path('single/product/<product_id>', get_single_product, name="single_product"),
    path('update/product/<product_id>', update_product, name="updated_product"),
    path('product/type/products', get_product_by_type, name="product_type_products"),
] + router.urls
