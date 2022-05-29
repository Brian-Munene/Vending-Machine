from django.conf.urls import url
from django.urls import path
from .views import RegisterUsers, login_view, make_maintainer


urlpatterns = [
      path('register', RegisterUsers.as_view(), name='register_user'),
      path('login', login_view, name='login_user'),
      path('make/maintainer', make_maintainer, name='make_maintainer')
]