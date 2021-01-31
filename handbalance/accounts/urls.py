from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_page),
    path('register', views.register_page),
    path('logout', views.logout_user),
    path('account', views.account_page)
]
