from django.db import models

# Create your models here.
class PizzaMenu(models.Model):
    type = models.CharField(max_length=32)
    size = models.CharField(max_length=10)
    topping_option = models.IntegerField() # 0(cheese), 1, 2, 3, 5 toppings
    price = models.FloatField()
    def __str__(self):
        topping_option_str = str(self.topping_option) + " toppings"
        if self.topping_option == 0:
            topping_option_str = 'cheese'
        return f"{self.id} - {self.type}, {self.size} with {topping_option_str} - ${self.price:.2f}"
class Pizza(PizzaMenu):
    toppings = models.ManyToManyField('Topping', blank=True, related_name="on_pizza")
    def __str__(self):
        topping_option_str = str(self.topping_option) + " toppings"

        if self.topping_option == 0:
            topping_option_str = 'cheese'
            message = f"{self.id} - {self.type}, {self.size} with {topping_option_str} - ${self.price:.2f}"
        # Has atleast one topping
        else:
            message = f"{self.id} - {self.type.capitalize()}, {self.size} with {topping_option_str} - ${self.price:.2f}\nTopping details:\n"
            for index, topping in enumerate(self.toppings.all()):
                message += str(index+1) + '. ' + topping.name + '\n';
        return message
class Topping(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.id} - {self.name}"
class SubMenu(models.Model):
    name = models.CharField(max_length=32)
    size = models.CharField(max_length=10)
    price = models.FloatField()
    def __str__(self):
        return f"{self.id} - {self.name}, {self.size} - ${self.price:.2f}"
class Sub(SubMenu):
    add_on = models.ManyToManyField('SubsAddOn', blank=True, related_name='on_sub')
    def __str__(self):
        message = f"{self.id} - {self.name}, {self.size} - ${self.price:.2f}"
        if len(self.add_on.all()):
            message += "\nAdd on details:\n"
        for index, addon in enumerate(self.add_on.all()):
            message += str(index+1) + '. ' + addon.name + '\n';
        return message
class SubsAddOn(models.Model):
    name = models.CharField(max_length=32)
    price = models.FloatField()
    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"
class PastaMenu(models.Model):
    name = models.CharField(max_length=32)
    price = models.FloatField()
    def __str__(self):
        return f"{self.id} - {self.name} - ${self.price:.2f}"
class Pasta(PastaMenu):
    pass
class SaladMenu(models.Model):
    name = models.CharField(max_length=32)
    price = models.FloatField()
    def __str__(self):
        return f"{self.id} - {self.name} - ${self.price:.2f}"
class Salad(SaladMenu):
    pass
class DinnerPlatterMenu(models.Model):
    name = models.CharField(max_length=32)
    size = models.CharField(max_length=10)
    price = models.FloatField()
    def __str__(self):
        return f"{self.id} - {self.name}, {self.size} - ${self.price:.2f}"
class DinnerPlatter(DinnerPlatterMenu):
    pass
class Order(models.Model):
    username = models.CharField(max_length=64)
    pizza = models.ManyToManyField(Pizza, blank=True, related_name='ordered')
    sub = models.ManyToManyField(Sub, blank=True, related_name='ordered')
    pasta = models.ManyToManyField(Pasta, blank=True, related_name='ordered')
    salad = models.ManyToManyField(Salad, blank=True, related_name='ordered')
    dinnerplatter = models.ManyToManyField(DinnerPlatter, blank=True, related_name='ordered')
    def sum_price(self, obj):
        this_sum = 0
        if len(obj.all()) > 0:
            for item in obj.all():
                this_sum += item.price
        return this_sum
    def total(self):
        total_sum = 0
        total_sum += self.sum_price(self.pizza)
        total_sum += self.sum_price(self.sub)
        total_sum += self.sum_price(self.pasta)
        total_sum += self.sum_price(self.salad)
        total_sum += self.sum_price(self.dinnerplatter)
        return round(total_sum, 2)
    def item_count(self):
        count = 0
        count += len(self.pizza.all())
        count += len(self.sub.all())
        count += len(self.pasta.all())
        count += len(self.salad.all())
        count += len(self.dinnerplatter.all())
        return count
    def __str__(self):
        return f"""id: {self.id} - {self.item_count()} item(s)-total {self.total()}"""
class CartSession(models.Model):
    username = models.CharField(max_length=150)
    cart_session = models.TextField()
    def __str__(self):
        return f"{self.id} - {self.username}"
