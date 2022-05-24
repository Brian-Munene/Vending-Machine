from django.urls import path
from rest_framework import routers
from .views import ProductTypeViewset

router = routers.DefaultRouter()
router.register(r'product/type', ProductTypeViewset, basename='product_type')

urlpatterns = [

              ] + router.urls
