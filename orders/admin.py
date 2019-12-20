from django.contrib import admin
from .models import PizzaMenu, Pizza, Topping, SubMenu, Sub, SubsAddOn, PastaMenu, Pasta, SaladMenu, Salad, DinnerPlatterMenu, DinnerPlatter, Order

# Register your models here.

admin.site.register(PizzaMenu)
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(SubMenu)
admin.site.register(Sub)
admin.site.register(SubsAddOn)
admin.site.register(PastaMenu)
admin.site.register(Pasta)
admin.site.register(SaladMenu)
admin.site.register(Salad)
admin.site.register(DinnerPlatterMenu)
admin.site.register(DinnerPlatter)
admin.site.register(Order)
