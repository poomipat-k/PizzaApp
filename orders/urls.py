from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("get_price", views.get_price, name="get_price"),
    path("add2cart", views.add2cart, name="add2cart")
]
