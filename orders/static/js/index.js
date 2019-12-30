document.addEventListener('DOMContentLoaded', function(){
// Get Topping data from django
let toppings_json = JSON.parse(document.querySelector("#topping_data").innerText);
let topping_option_select = document.querySelector("#PizzaMenu_topping_option");
let sub_select_name = document.querySelector("#SubMenu_name");
let sub_add_on = JSON.parse(document.querySelector("#sub_add_on").innerText);
var topping_options = document.querySelectorAll(".option_dropdown");
var sub_add_on_added = [];
// Vairable to manage topping dropdown disabled/enable
const MAX_TOPPING_OPTION = 5;
var selected_toppings = {};
for (let i = 0; i < MAX_TOPPING_OPTION; i++){
  selected_toppings[`topping${i+1}`] = '';
}

var SUB_ADD_ON_STATE = [];

update_topping();
// Dynamicly add Topping select dropdown per topping_option from user input
topping_option_select.addEventListener('change', function(){
  update_topping();
  // Enable add to cart button when toppings are fully selected
  disable_Pizza_add2cart();
});

// Listen to topping change event then update selected_toppings vaiable and disable/enable topping option
document.querySelector("#topping_dropdown").addEventListener("change", function(e){
  if (e.target && e.target.id.startsWith("topping")){
    selected_toppings[e.target.id] = e.target.value;
  }
  // Update toppings dropdown state from selected_toppings global variables
  // Iterate all of over topping select tags
  for (let ele of e.target.parentElement.children){
    // Filter element with its id starts with "topping"
    if (ele.id.startsWith("topping")){
      // Iterate over all option tags and set disable to
      for (let row of ele.children){
        if (row.value){
          row.disabled = false;
        }
      }
      // For each key of selected_toppings, disabled them all
      for (let key in selected_toppings){
        if (selected_toppings[key] != ""){
          // Disabled option that is in selected_toppings
          let b = document.querySelector(`#${ele.id}_${selected_toppings[key].replace(" ", "_")}`);
          if (b){
            b.disabled = true;
          }
        }
      }
    }
  }
  disable_Pizza_add2cart();
});
disable_Pizza_add2cart();

update_sub_add_on();
update_sub_add_on_buttons();
sub_select_name.addEventListener('change', function(){
  update_sub_add_on();
  document.querySelectorAll(".add_on").forEach(function(button){
    button.classList.remove('added');
  });
});
// Disable small size option of Sub which name is
// Sausage,Peppers and Onions which available on large size only
let submenu_select = document.querySelector("#SubMenu_name");
submenu_select.addEventListener('change', function(){
  if (submenu_select.value.trim() == "Sausage, Peppers and Onions"){
    document.querySelector("#SubMenu_size").innerHTML = `<option class="" value="large">large</option>`;
  }
  else{
    document.querySelector("#SubMenu_size").innerHTML = `
    <option class="" value="large">large</option>
    <option class="" value="small">small</option>
    `;
  }
});

// Update price of the button for any change
let all_select = document.querySelectorAll("select");
all_select.forEach(function(select){
  // Initialize price in button
  get_price(select);
  // Listen to change event then update the price in add to cart button
  select.addEventListener('change', function(){
    get_price(this);
    if (select.id == 'SubMenu_size' || select.id == 'SubMenu_name'){
      document.querySelectorAll(".add_on").forEach(function(button){
        button.classList.remove('added');
        button.dataset.added = 'false';
        SUB_ADD_ON_STATE = [];
        });
      }
  });
});

// Listen to click event on add2cart button then add the item to cart
document.querySelectorAll(".add2cart_button").forEach(function(button){
  button.addEventListener("click", function(){
    // In case sub menu was click include add_on data sending to server too
    if (button.id.startsWith("SubMenu")){
      SUB_ADD_ON_STATE = [];
      for (let ele of document.querySelectorAll(".add_on")){
        if (ele.dataset.added == 'true'){
          SUB_ADD_ON_STATE.push(ele.dataset.name);
        }
      }
    }
    add2cart(this);
  })
});

function getCookie(name) {
var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
// Get cookie
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
// Set up default csrf token
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Ajax post request function
function post_request(url, callback, data){
  $.ajax({
    url : url,
    success : callback,
    type : "POST",
    data : data
  });
}
// Add item to cart
function add2cart(button){
  url = "/add2cart";
  callback = function(result){
    console.log(result);
  }
  data = get_data_to_submit(button);
  post_request(url, callback, data);
}

// Dynamicly add select dropdowns for pizza's topping
function update_topping(){
  let topping_dropdown = document.querySelector("#topping_dropdown");
  let n = Number(topping_option_select.value);
  let html = '';
  if (n > 0){
    for (let i = 0; i < n; i++){
      html += `
      <label style="color: #31a62b; position: relative; left: 44px;">Topping ${i+1}</label>
      <select id="topping${i+1}" class="option_dropdown topping_class" name="topping${i+1}">
      <option id="topping${i+1}_none" value="" disabled selected style="color: lightgray;"></option>
      `;
      for (let cell of toppings_json){
        html += `<option id="topping${i+1}_${cell.replace(" ", "_")}" value="${cell}">${cell}</option>`;
      }
      html += `</select><br>`;
    }
    topping_dropdown.innerHTML = html;
  }
  else{
    topping_dropdown.innerHTML = '';
  }
  // Clear all selected_toppings[key] to ''
  for (let key in selected_toppings){
    selected_toppings[key] = '';
  }
}
// Add sub add button on when Steak + Cheese is selected
function update_sub_add_on(){
  // Update additional add on for Steak and Cheese
  let sub_add_on_div = document.querySelector("#sub_add_on_div");
  let add_on_buttons = document.querySelectorAll('.add_on');
  if (sub_select_name.value.trim() == "Steak and Cheese"){
    // Steak and Cheese show 3 more add ons
    for (let item of add_on_buttons){
      if (item.dataset.name != "Extra Cheese"){
        item.classList.remove('hidden');
      }
    }
  }
  // Steak and Cheese option not selected, hide 3 add ons
  else{
    for (let item of add_on_buttons){
      if (item.dataset.name != "Extra Cheese"){
        item.classList.add('hidden');
      }
    }
  }
}
function get_price(select_button){
  // Get django models name from select_button id
  let model_name = select_button.id.split('_')[0]; // PizzaMenu
  // Get HTML tags that has id startswith model_name
  let attribute_select_tag = [];
  for (let item of all_select){
    if (item.id.startsWith(model_name)){
      attribute_select_tag.push(item);
    }
  }
  // Extract attribute name from tags
  let attr_list = [];
  for (let tag of attribute_select_tag){
    let attr_name = '';
    let tag_id = tag.id.split('_');
    for (let i = 1; i < tag_id.length; i++){
      attr_name += tag_id[i] + '_';
    }
    attr_name = attr_name.slice(0,-1);
    attr_list.push(attr_name)
  }
  // Prepare data to send to server
  let attributes = {'model_name' : model_name}
  for (let att of attr_list){
    let node = document.querySelector("#" + model_name + '_' + att);
    attributes[att] = node.value;
  }
  // Make AJAX request to server via GET request to get the price for the item
  const request = new XMLHttpRequest();
  let url = "/get_price?";
  for (let att in attributes){
    url += att + '=' + attributes[att] + '&';
  }
  url = url.slice(0,-1);
  // Callback function
  request.onload = function(){
    let button = document.querySelector("#" + model_name + '_price')
    button.dataset.price = request.responseText;
    button.innerHTML = '+$' + request.responseText + ' to Cart';
  };
  request.open("GET", url);
  request.send();
}
function update_sub_add_on_buttons(){
  // add-on buttons
  let b = document.querySelectorAll(".add_on");
  // add2cart_button
  let add2cart = document.querySelector("#SubMenu_price");
  b.forEach(function(button){
    button.addEventListener("click", function(){
      let added = false;
      for (let cls of button.classList){
        if (cls == "added"){
          added = 'true';
        }
      }
      // Has "added" class
      if (added){
        button.classList.remove('added');
        button.innerText = `+$${button.dataset.price} ${button.dataset.name}`
        button.dataset.added = 'false';
        // Subtract
        add2cart.dataset.price = parseFloat(add2cart.dataset.price) - parseFloat(button.dataset.price);
        add2cart.innerText = `+$${Math.round(add2cart.dataset.price * 100) / 100} to Cart`;
      }
      else{
        button.classList.add('added');
        button.innerText = `-$${button.dataset.price} ${button.dataset.name}`
        button.dataset.added = true;
        // Plus
        add2cart.dataset.price = parseFloat(add2cart.dataset.price) + parseFloat(button.dataset.price);
        add2cart.innerText = `+$${Math.round(add2cart.dataset.price * 100) / 100} to Cart`;
      }
  });
});
}
function disable_Pizza_add2cart(){
  let topping_qty = document.querySelector("#PizzaMenu_topping_option").value;
  let count = 0;
  for (let key in selected_toppings){
    if (selected_toppings[key]){
      count += 1;
    }
  }
  // Enable add to cart button
  if (count == Number(topping_qty)){
      document.querySelector("#PizzaMenu_price").disabled = false;
  }
  else{
    document.querySelector("#PizzaMenu_price").disabled = true;
  }
}
// Get data of the item that was click to add to cart
function get_data_to_submit(button){
  let item_name = button.id.split("_")[0];
  let attr_tag = document.querySelectorAll(`.${item_name}_div .option_dropdown`);
  let data = {
    'model_name' : item_name,
  };
  for (let tag of attr_tag){
    let key = tag.id.replace(`${item_name}_`,``);
    let value = tag.value;
    data[key] = value;
  }
  // Additional infomation for SubMenu model
  // Add on data
  data['addon'] = JSON.stringify(SUB_ADD_ON_STATE);
  return data;
}
});
