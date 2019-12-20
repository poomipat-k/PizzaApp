from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.urls import reverse
from .models import PizzaMenu, Topping
import json

# Create your views here.
# Index page
def index(request):
    # User not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    # User has logged ins
    types, topping_option, size = set(), set(), set()
    # Fetch data from PizzaMenu
    for item in PizzaMenu.objects.all():
        types.add(item.type)
        topping_option.add(item.topping_option)
        size.add(item.size)
    menu = {
        'type' : sorted(tuple(types)),
        'topping_option' : sorted(tuple(topping_option)),
        'size' : sorted(tuple(size), reverse=True)
        }
    # Fetch data from Topping
    toppings= set()
    for item in Topping.objects.all():
        toppings.add(item.name)
    toppings = sorted(tuple(toppings))

    # Count item on cart
    count = 0
    try:
        for key in request.session['cart']:
            count += len(request.session['cart'][key])
    except KeyError:
        pass

    contect = {
        "user" : request.user,
        "menu" : menu,
        "toppings" : toppings,
        "topping_json" : json.dumps(toppings),
        "item_on_cart" : count
    }
    return render(request, "orders/index.html", contect)

def get_pizza_price(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            raise Http404("Wrong request method")
        types = request.GET['t']
        size = request.GET['s']
        topping_option = request.GET['topping']
        price = PizzaMenu.objects.filter(type=types, size=size, topping_option=topping_option)[0].price
        return HttpResponse(price)
    else:
        raise Http404("Not logged in.")

def add_pizza_to_cart(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            raise Http404("Wrong request method")
        # Create a new session key called 'cart'
        types = request.GET['types']
        size = request.GET['size']
        topping_option = request.GET['topping_option']
        price = request.GET['price']
        toppings = []
        for i in range(int(topping_option)):
            this_topping = 'topping' + str(i+1)
            toppings.append(request.GET[this_topping])

        # No keyword cart in session
        if 'cart' not in request.session:
            request.session['cart'] = {}
            request.session['cart']['pizza'] = []
            request.session['cart']['pizza'].append({
            'types' : types,
            'size' : size,
            'topping_option' : topping_option,
            'toppings' : toppings,
            'price' : price
            })
            request.session.modified = True
            count = 0
            for key in request.session['cart']:
                count += len(request.session['cart'][key])
            return HttpResponse(count)
        # There is/are items in the cart already
        else:
            count = 0
            if len(request.session['cart']['pizza']) > 0:
                request.session['cart']['pizza'].append({
                'types' : types,
                'size' : size,
                'topping_option' : topping_option,
                'toppings' : toppings,
                'price' : price
                })
                request.session.modified = True
            for key in request.session['cart']:
                count += len(request.session['cart'][key])
            return HttpResponse(count)
    # Not logged in raise error
    else:
        raise Http404("Not logged in.")

def clear(request):
    if request.user.is_authenticated:
        del request.session['cart']
        if 'cart' not in request.session:
            return HttpResponse('success')
        else:
            return HttpResponse('failure')
    else:
        raise Http404("Not logged in.")

def checkout(request):
    if request.user.is_authenticated:
        data = json.dumps(request.session['cart'])
        # Count item on cart
        count = 0
        try:
            for key in request.session['cart']:
                count += len(request.session['cart'][key])
        except KeyError:
            pass
        contect = {
        'data' : data,
        'item_on_cart' : count
        }
        return render(request, 'orders/checkout.html', contect)
    else:
        raise Http404("Not logged in")

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
    logout(request)
    return render(request, "orders/login.html", {"message" : "Logged out."})

def signup(request):
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
