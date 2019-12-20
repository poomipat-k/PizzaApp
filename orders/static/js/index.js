document.addEventListener('DOMContentLoaded', function(){
  // Type
  let type = document.querySelector("#type");
  // Size
  let size = document.querySelector("#size");
  // Topping_option
  let topping_option = document.querySelector("#topping_option");
  let topping_dropdown = document.querySelector('#topping_option_dropdown');
  var price;
  let checkout = document.querySelector("#checkout");
  let clear = document.querySelector("#clear");

  // Change cart color in navbar when there are item on cart
  function cart_update(){
    let cart_nav = document.querySelector("#cart")
    // True if there are items in the cart
    if (parseInt(cart_nav.innerHTML) > 0){
      cart_nav.style.color = "red";

      // Add classname inactiveLink to disable checkout link
      let inactive_checkout = is_inactive(checkout);
      // Has inactiveClass
      if (inactive_checkout){
        checkout.classList.remove("inactiveLink");
      }

      let inactive_clear = is_inactive(clear);
      if (inactive_clear){
        clear.classList.remove("inactiveLink");
      }
    }
    // Cart is empty
    else {
      cart_nav.style.color = '';
      let inactive_checkout = is_inactive(checkout);
      // Does not have inactiveLing class
      if (!inactive_checkout){
        checkout.classList.add("inactiveLink");
      }

      // Does not have inactiveLing class
      let inactive_clear = is_inactive(clear);
      if (!inactive_clear){
        clear.classList.add("inactiveLink");
      }
    }
    // Function to check if the element has inactiveLink class
    function is_inactive(element)
    {
      let inactive = false;
      for (let i of element.classList){
        if (i == 'inactiveLink'){
          inactive = true;
        }
      }
      return inactive;
    }
    }

  cart_update();

  // Dynamics add dropdown selections from user input's topping_option
  let topping_json = JSON.parse(document.getElementById('topping_json').textContent);
  topping_json = JSON.parse(topping_json);
  topping_option.addEventListener("change", function(){
    html = '';
    for (let i = 0; i < topping_option.value; i++){
      html += "<label>" + "Topping " + (i+1) + ": " + "</label>";
      html += "<select id=" + "topping" + (i+1) + ">";
      for (let item of topping_json){
        html += '<option>' + item + '</option>';
      }
      html += "</select><br>";
    }
    topping_dropdown.innerHTML = html;
  });
  // Get pizza price when the page is reloaded
  get_pizza_price();

  // Get the pizza price when dropdown value is changed
  let pizza_cart_button = document.querySelector("#pizza_cart");
  type.addEventListener('change', function(){
    get_pizza_price();
  });
  size.addEventListener('change', function(){
    get_pizza_price();
  });
  topping_option.addEventListener('change', function(){
    get_pizza_price();
  });
  function get_pizza_price()
  {
    let request = new XMLHttpRequest();
    request.onload = function(){
      price = JSON.parse(request.responseText);
      pizza_cart_button.innerHTML = "Add to cart: " + price + " dollars";
    };
    let selected_type = type.value;
    let selected_size = size.value;
    let selected_topping_option = topping_option.value;
    let url = '/get_pizza_price?t=' + selected_type + '&s=' + selected_size + '&topping=' + selected_topping_option;
    request.open('GET', url);
    request.send();
  }

  // Add to cart action
  pizza_cart_button.addEventListener('click', function(){
    // Send Ajax request to server to set shopping cart session
    let request = new XMLHttpRequest();
    let count;
    request.onload = function(){
      count = request.responseText;
      // Add number of item in vitual shopping cart in navbar
      let cart = document.querySelector("#cart");
      if (parseInt(count) === 1){
        cart.innerHTML = "1 item in Cart";
        cart_update();
      }
      else if (parseInt(count) > 1){
        cart.innerHTML = count + " items in Cart"
        cart_update();
      }

    };

    let url = '/add_pizza_to_cart?';
    let info = {
      'types' : type.value,
      'size' : size.value,
      'topping_option' : topping_option.value,
      'price' : price,
      }
    for (let i = 0; i < topping_option.value; i++){
      let id_code = "topping" + (i+1);
      info[id_code] = document.querySelector("#" + id_code).value;
    }
    for (let key in info){
      url += key + '=' + info[key] + '&';
    }
    url = url.slice(0,-1);
    request.open('GET', url);
    request.send();

  });

  // Clear items in Cart
  let clear_link = document.querySelector("#clear");
  clear_link.addEventListener("click", function(evt){
    evt.preventDefault();
    let request = new XMLHttpRequest();
    let url = "/clear"
    request.onload = function(){
      let data = request.responseText;
      if (data.trim() === "success"){
        // Remove number of item in cart and update the font color
        let cart = document.querySelector("#cart");
        cart.innerHTML = "Cart";
        cart_update();
      }

    }
    request.open("GET", url)
    request.send()
  });

});
