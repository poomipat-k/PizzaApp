from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.urls import reverse
from .models import PizzaMenu, Pizza, Topping, SubMenu, Sub, SubsAddOn, PastaMenu, Pasta
from .models import SaladMenu, Salad, DinnerPlatterMenu, DinnerPlatter, Order, CartSession
import json
from urllib.parse import unquote, unquote_plus

# When add class in model.py, you need to manually add data in these three variables
# 'unrelated_att', 'menu_class', 'menu_class_str'
# Order of menu_class and menu_class_str must identical
unrelated_att = ['DoesNotExist', 'MultipleObjectsReturned',
'objects', 'id', 'pizza', 'on_pizza', 'price',
'sub', 'on_sub', 'pasta', 'salad', 'dinnerplatter']
menu_class = [PizzaMenu, SubMenu, PastaMenu, SaladMenu, DinnerPlatterMenu]
menu_class_str = ['PizzaMenu', 'SubMenu', 'PastaMenu', 'SaladMenu', "DinnerPlatterMenu"]

def generate_menu():
    """Return Menu, Topping, SubsAddOn"""
    # For Menu
    menu_data = {}
    for index, item in enumerate(menu_class):
        # Get in PizzaMenu class
        if len(menu_class) != len(menu_class_str):
            return HttpResponse("Error: menu_class and menu_class_str size not identical")
        item_name = menu_class_str[index]
        item_att = [att for att in item.__dict__.keys() if not att.startswith('_')
                    and att not in unrelated_att]
        menu_data[item_name] = {}
        for att in item_att:
            att_data_set = set()
            for row in item.objects.all():
                att_data_set.add(getattr(row, att))
            menu_data[item_name][att] = sorted(list(att_data_set))
        # Pizza topping variable
        toppings = set()
        for topping in Topping.objects.all():
            toppings.add(topping.name)
        toppings = sorted(list(toppings))
        # Subs add on variable
        sub_add_on = []
        for item in SubsAddOn.objects.all():
            sub_add_on.append({'name' : item.name, 'price' : round(item.price, 2)})
    return menu_data, toppings, sub_add_on
# Generate menu data
MENU = generate_menu()
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        menu = MENU[0]
        toppings = MENU[1]
        sub_add_on = MENU[2]
        # Store all info in contect, prepare to pass to html page
        contect = {
        'message' : None,
        'unrelated_attr' : unrelated_att,
        'menu_json' : json.dumps(MENU),
        'menu' : menu,
        'toppings' : toppings,
        'sub_add_on' : sub_add_on
        }
        return render(request, 'orders/index.html', contect)
    else:
        contect = {
        'message' : None
        }
        return HttpResponseRedirect(reverse('login'))

def login_view(request):
    logout(request)
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message" : "Invalid credential"})
    # Reach via GET request
    else:
        return render(request, "orders/login.html", {"message":None})
def logout_view(request):
    # Resever for save session
    logout(request)
    contect = {
    'message' : 'Logged out.'
    }
    return render(request, "orders/login.html", contect)
def signup(request):
    if request.user.username:
        logout(request)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            form = SignUpForm()
            contect = {
            'form' : form
            }
            return render(request, 'orders/signup.html', contect)
    # Reach via GET request
    else:
        form = SignUpForm()
        contect = {
        'form' : form
        }
    return render(request, 'orders/signup.html', contect)
def get_price(request):
    """Get price from django model"""
    if request.user.is_authenticated:
        try:
            model_name = request.GET["model_name"]
        except KeyError:
            return render(request, "orders/error.html", {'message' : "Key Error: No model name"})
        model_index = menu_class_str.index(model_name)
        model = menu_class[model_index]
        attributes = [att for att in model.__dict__.keys() if not att.startswith('_')
                     and att not in unrelated_att]
        filter_data = {}
        for att in attributes:
            try:
                filter_data[att] = unquote_plus(request.GET[att])
            except KeyError:
                return render(request, "orders/error.html", {'message' : f"Key Error: {att}"})
            except IndexError:
                return render(request, "orders/error.html", {'message' : f"IndexError list index out of range: {att}"})
        price = model.objects.filter(**filter_data)[0].price
        return HttpResponse(f"{price:.2f}")
    else:
        raise Http404("Not logged in")
def add2cart(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                model_name = request.POST['model_name']
            except KeyError:
                return render(request, "orders/error.html", {"message" : "Key error: model_name"})
            model_index = menu_class_str.index(model_name)
            model = menu_class[model_index]
            # Get attribute
            attr = [att for att in model.__dict__.keys() if not att.startswith('_')
                         and att not in unrelated_att]
            # Get price from backend models to ensure the price
            data = {}
            for att in attr:
                try:
                    data[att] = request.POST[att]
                except KeyError:
                    return render(request, "orders/error.html", {'message' : f"Key Error: {att}"})
            try:
                price = model.objects.filter(**data)[0].price
            except IndexError:
                return render(request, "orders/error.html", {'message' : f"IndexError: Item not in Menu"})
            # Get username
            username = request.user.username
            # SubMenu model, add addon data to 'data' variable
            if (model_name == "SubMenu"):
                # Add additional cost to total price, $0.50 per add on
                data['addon'] = sorted(list(set(json.loads(request.POST['addon']))))
                price += round(0.5 * len(data['addon']), 2)

            # PizzaMenu model, add toppings data to 'data' variable
            if (model_name == "PizzaMenu"):
                topping_option = int(data['topping_option'])
                toppings = []
                for i in range(topping_option):
                    toppings.append(request.POST[f"topping{i+1}"])
                data['toppings'] = toppings
                if len(toppings) != topping_option:
                    return render(request, 'orders/error.html', {'message' : 'Topping quantity not correct.'})
            return JsonResponse(data, safe=False)
        else:
            return render(request, "orders/error.html", {'message' : "Wrong request"})
    else:
        return render(request, "orders/error.html", {'message': "Please log in"})
