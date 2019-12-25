document.addEventListener('DOMContentLoaded', function(){
  // Get Topping data from django
  let toppings_json = JSON.parse(document.querySelector("#topping_data").innerText);
  let topping_option_select = document.querySelector("#PizzaMenu_topping_option");
  let sub_select = document.querySelector("#SubMenu_name");
  let sub_add_on = JSON.parse(document.querySelector("#sub_add_on").innerText);

  update_topping();
  topping_option_select.addEventListener('change', function(){
    update_topping()
  });

  update_sub_add_on();
  sub_select.addEventListener('change', function(){
    update_sub_add_on();
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

  let all_select = document.querySelectorAll("select");
  all_select.forEach(function(select){
    // Initialize price in button
    get_price(select);
    // Listen to change event then update the price in add to cart button
    select.addEventListener('change', function(){
      get_price(this);
    });
  });

  // Dynamicly add select dropdowns for pizza's topping
  function update_topping(){
    let topping_dropdown = document.querySelector("#topping_dropdown");
    let n = Number(topping_option_select.value);
    let html = '';
    if (n > 0){
      for (let i = 0; i < n; i++){
        html += `
        <div style="margin-top:3px; margin-bottom:3px;">
        <label style="color: #31a62b; position: relative; left: 44px;">Topping ${i+1}</label>
        <select id="topping${i}" class="option_dropdown" name="topping${i}">
        `;
        for (let cell of toppings_json){
          html += `<option value="${cell}">${cell}</option>`;

        }
        html += `</select><br></div>`;
      }
      topping_dropdown.innerHTML = html;
    }
    else{
      topping_dropdown.innerHTML = '';
    }
  }

  function update_sub_add_on(){
    let sub_add_on_div = document.querySelector("#sub_add_on_div");
    html = ``;
    if (sub_select.value.trim() == "Steak and Cheese"){
      html += `<div class="btn-group" role="group" aria-label="Basic example">`;
      for (let info of sub_add_on){
        if (info.name != "Extra Cheese"){
          html += `<button type="button" class="btn btn-success">+${info.price} ${info.name}</button>`;
        }
      }
      html += `</div>`;
    }
    sub_add_on_div.innerHTML = html;
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
      attributes[att] = [node.value];
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
      document.querySelector("#" + model_name + '_price').innerHTML = '+$' +
      request.responseText + ' to Cart';
    };
    request.open("GET", url);
    request.send();
  }
});
