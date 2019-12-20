from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("get_pizza_price", views.get_pizza_price, name='pizza_price'),
    path("add_pizza_to_cart", views.add_pizza_to_cart, name='pizza_cart'),
    path("clear", views.clear, name='clear'),
    path("checkout", views.checkout, name='checkout')
]
