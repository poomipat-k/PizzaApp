from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.urls import reverse
from .models import *
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
# Cart session data structure
model_classes = [PizzaMenu, Pizza, Topping, SubMenu, Sub, SubsAddOn, PastaMenu, Pasta,
                 SaladMenu, Salad, DinnerPlatterMenu, DinnerPlatter, Order, CartSession]
def new_cart():
    init_cart = {}
    for item in menu_class_str:
        init_cart[item[:-4]] = []
    return init_cart
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
        # Count how many item in cart
        cart_item_count = 0
        try:
            for k in request.session['cart'].keys():
                cart_item_count += len(request.session['cart'][k])
        except KeyError:
            pass
        # Store all info in contect, prepare to pass to html page
        contect = {
        'message' : None,
        'unrelated_attr' : unrelated_att,
        'menu_json' : json.dumps(MENU),
        'menu' : menu,
        'toppings' : toppings,
        'sub_add_on' : sub_add_on,
        'cart_count' : cart_item_count
        }
        return render(request, 'orders/index.html', contect)
    else:
        contect = {
        'message' : None
        }
        return HttpResponseRedirect(reverse('login'))

def login_view(request):
    if request.user.is_authenticated:
        """Save logged in user's session data"""
        # Push session data to database before log a userout
        username = request.user.username
        # No cart session of the user in database
        if (len(CartSession.objects.filter(username=username)) == 0 ):
            try:
                cart_session_data = CartSession(username=username, cart_session=json.dumps(request.session['cart']))
                cart_session_data.save()
            except KeyError:
                pass
        # Cart session data of this user already exist in the database
        else:
            # Error check if one user has many cart session
            if len(CartSession.objects.filter(username=username)) > 1:
                return render(request, 'orders/error.html', {'message' : 'More than one cart session exist in database'})
            try:
                c = CartSession.objects.filter(username=username)[0]
                c.cart_session = json.dumps(request.session['cart'])
                c.save()
            except KeyError:
                pass
    # Logout request
    logout(request)
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Initialize cart session
            request.session['cart'] = new_cart()
            # Pull cart session data from database
            try:
                fetched_session = CartSession.objects.filter(username=request.user.username)[0]
                request.session['cart'] = json.loads(fetched_session.cart_session)
            except IndexError:
                # Error catch when user has no cart session in database
                pass
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message" : "Invalid credential"})
    # Reach via GET request
    else:
        return render(request, "orders/login.html", {"message":None})
def logout_view(request):
    # Push session data to database before log a userout
    username = request.user.username
    # No cart session of the user in database
    if (len(CartSession.objects.filter(username=username)) == 0 ):
        try:
            cart_session_data = CartSession(username=username, cart_session=json.dumps(request.session['cart']))
            cart_session_data.save()
        except KeyError:
            pass
    # Cart session data of this user already exist in the database
    else:
        # Error check if one user has many cart session
        if len(CartSession.objects.filter(username=username)) > 1:
            return render(request, 'orders/error.html', {'message' : 'More than one cart session exist in database'})
        try:
            c = CartSession.objects.filter(username=username)[0]
            c.cart_session = json.dumps(request.session['cart'])
            c.save()
        except KeyError:
            pass
    logout(request)
    contect = {
    'message' : 'Logged out.'
    }
    return render(request, "orders/login.html", contect)
def signup(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            """Save logged in user's session data"""
            # Push session data to database before log a userout
            username = request.user.username
            # No cart session of the user in database
            if (len(CartSession.objects.filter(username=username)) == 0 ):
                try:
                    cart_session_data = CartSession(username=username, cart_session=json.dumps(request.session['cart']))
                    cart_session_data.save()
                except KeyError:
                    pass
            # Cart session data of this user already exist in the database
            else:
                # Error check if one user has many cart session
                if len(CartSession.objects.filter(username=username)) > 1:
                    return render(request, 'orders/error.html', {'message' : 'More than one cart session exist in database'})
                try:
                    c = CartSession.objects.filter(username=username)[0]
                    c.cart_session = json.dumps(request.session['cart'])
                    c.save()
                except KeyError:
                    pass
        # Logout request
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
                data['add_on'] = sorted(list(set(json.loads(request.POST['add_on']))))
                price += round(0.5 * len(data['add_on']), 2)

            # PizzaMenu model, add toppings data to 'data' variable
            if (model_name == "PizzaMenu"):
                topping_option = int(data['topping_option'])
                toppings = []
                for i in range(topping_option):
                    toppings.append(request.POST[f"topping{i+1}"])
                data['toppings'] = toppings
                if len(toppings) != topping_option:
                    return render(request, 'orders/error.html', {'message' : 'Topping quantity not correct.'})
            # Append model_name in data
            data['model_name'] = model_name
            # Append price in model
            data['price'] = price
            # Add data to cart session
            if 'cart' not in request.session:
                # Initialize a cart data
                request.session['cart'] = new_cart()
                request.session.modified = True
                # Add data to cart
                data_to_session = {k:v for k,v in data.items() if k != "model_name"}
                request.session['cart'][model_name[:-4]].append(data_to_session)
                # Save nested data structure in session
                request.session.modified = True

            # Cart session already exist
            else:
                data_to_session = {k:v for k,v in data.items() if k != "model_name"}
                request.session['cart'][model_name[:-4]].append(data_to_session)
                # Save nested data structure in session
                request.session.modified = True
            # Count how many item in cart
            cart_item_count = 0
            try:
                for k in request.session['cart'].keys():
                    cart_item_count += len(request.session['cart'][k])
            except KeyError:
                pass

            return JsonResponse(cart_item_count, safe=False)
        else:
            return render(request, "orders/error.html", {'message' : "Wrong request"})
    # User not logged in
    else:
        return render(request, "orders/error.html", {'message': "Please log in"})
def clear_cart(request):
    request.session['cart'] = new_cart()
    # response = {'success' : True}
    # return JsonResponse(response)
    return HttpResponseRedirect(reverse("index"))
def checkout(request):
    # Count how many item in cart
    cart_item_count = 0
    try:
        for k in request.session['cart'].keys():
            cart_item_count += len(request.session['cart'][k])
    except KeyError:
        pass
    # Get cart session data
    cart_data = new_cart()
    try:
        cart_data = request.session['cart']
    except KeyError:
        pass
    # Get total price of the items in the cart
    total = 0
    try:
        for item_type in cart_data:
            for row in cart_data[item_type]:
                total += row['price']
    except KeyError:
        pass
    contect = {
    'cart_count' : cart_item_count,
    'cart_data' : cart_data,
    'total' : round(total,2)
    }
    return render(request, "orders/checkout.html", contect)
def place_order(request):
    if request.user.is_authenticated and request.method == "POST":
        data = {}
        username = request.user.username
        try:
            data = request.session['cart']
        except KeyError:
            pass
        message = 'init'
        # If data is not blank
        if data:
            # Create order
            order = Order(username=username)
            order.save()
            for key in data.keys():
                # key = "Pizza"
                for item in data[key]:
                    # Normal field attributes
                    att = {k:v for k,v in item.items() if k != "toppings" and k != "add_on"}
                    # ManyToManyField attributes
                    att_list_object = {k:v for k,v in item.items() if k == "toppings" or k == "add_on"}
                    # Select model
                    model_item = [m for m in model_classes if m.__name__ == key][0]
                    # Create object
                    new_obj = model_item(**att)
                    new_obj.save()
                    # Add toppings to Pizza or add ons to Sub
                    for k, v in att_list_object.items():
                        for row in v:
                            # In case k is toppings
                            if k == 'toppings':
                                try:
                                    addition = Topping.objects.filter(name=row)[0]
                                    addition.save()
                                except:
                                    pass
                            # In case k is add_on
                            elif k == 'add_on':
                                try:
                                    addition = SubsAddOn.objects.filter(name=row)[0]
                                    addition.save()
                                except:
                                    pass
                            getattr(new_obj, k).add(addition)
                            new_obj.save()
                    getattr(order, key.lower()).add(new_obj)
                    order.save()
            request.session['cart'] = new_cart()
            return JsonResponse("Order confirmed", safe=False)
        # Cart session data is blank
        else:
            return JsonResponse("Fail, cart session blank", safe=False)
    else:
        return render(request, 'orders/error.html', {'message' : "Not logged in or wrong request method"})
def order_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        interested_att = ['pizza','sub','pasta','salad','dinnerplatter']
        order_all = Order.objects.all()
        # Count how many item in cart
        cart_item_count = 0
        try:
            for k in request.session['cart'].keys():
                cart_item_count += len(request.session['cart'][k])
        except KeyError:
            pass
        complete_order = []
        pending_order = []
        for order in order_all:
            if order.is_complete:
                complete_order.append(order)
            else:
                pending_order.append(order)
        contect = {
        'order_data' : order_all,
        'cart_count' : cart_item_count,
        'complete_order' : complete_order,
        'pending_order' : pending_order
        }
        return render(request, 'orders/order_view.html', contect)
    else:
        return render(request, 'orders/error.html', {'message':'Can not access to this page'})
def order_details(request, order_id):
    if request.user.is_authenticated and request.user.is_staff:
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
        # Count how many item in cart
        cart_item_count = 0
        try:
            for k in request.session['cart'].keys():
                cart_item_count += len(request.session['cart'][k])
        except KeyError:
            pass
        contect = {
        'order_id' : order_id,
        'customer_name' : order.username,
        'pizza' : order.pizza.all(),
        'sub' : order.sub.all(),
        'pasta' : order.pasta.all(),
        'salad' : order.salad.all(),
        'dinnerplatter' : order.dinnerplatter.all(),
        'cart_count' : cart_item_count,
        'is_complete' : order.is_complete
        }
        return render(request, 'orders/order_details.html', contect)
    else:
        return render(request, 'orders/error.html', {'message': "Can not access"})

def change_order_status(request):
    if request.method == "POST" and request.user.is_authenticated and request.user.is_staff:
        try:
            order_id = int(request.POST["order_id"])
        except KeyError:
            pass
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            raise Http404(f"Order id: {order_id} does not exist")
        try:
            status = request.POST["status"]
        except KeyError:
            pass
        if status == "complete":
            order.is_complete = True
        else:
            order.is_complete = False
        order.save()
        return HttpResponse("Order is complete")

    else:
        return render(request, 'orders/error.html', {'message' : "Not logged in"})
