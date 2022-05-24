from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
import accounts.urls as account_urls
import products.urls as product_urls
import coins.urls as coin_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token', jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include(account_urls)),
    path('products/', include(product_urls)),
    path('coins/', include(coin_urls)),
]
