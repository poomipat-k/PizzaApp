document.addEventListener("DOMContentLoaded", function(){
  let data = JSON.parse(document.getElementById('data').textContent);
  data_json = JSON.parse(data);
  let total = JSON.parse(document.getElementById('total').textContent);
  total = JSON.parse(total);
  let cart = document.querySelector("#cart");
  // Hidden cart's navbar dropdown
  cart.hidden = true;

  let content = document.querySelector("#content");
  // Atleast one pizza cart
  if (data_json){
    var html = `
    <h2>Pizza</h2>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Type</th>
          <th scope="col">Size</th>
          <th scope="col">Toppings</th>
          <th scope="col">Price</th>
        </tr>
      </thead>
      `;
    for (item_key in data_json){
      for (let index in data_json[item_key]){
        html += `<tr><td>` + (Number(index) + 1) + `</td>`;
        for (let att in data_json[item_key][index]){
          if (att == "topping_option"){
            continue;
          }
          if (att == "toppings"){
            html += `<td>`
            for (let topping of data_json[item_key][index][att]){
              html += `<pre>` + topping + `</pre>`;
  				  }
            if (data_json[item_key][index][att].length == 0 ){
              html += `Cheese`;
            }
            html += `</td>`
  			  }
          else{
            html += `<td>` + data_json[item_key][index][att] + `</td>`;
          }
        }
        html += `
        <td><button type="button" class="btn btn-danger">Delete</button></td>
        </tr>
        `;
      }
    }
    html += `</table><hr>`;
  }
  let total_div = document.querySelector("#total_div");
  total_div.innerHTML = '<h2>$' + total + '</h2>';
  content.innerHTML = html;
});
