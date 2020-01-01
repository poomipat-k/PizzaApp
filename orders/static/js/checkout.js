document.addEventListener("DOMContentLoaded", function(){
  // Nav link functionality without include #Pizza in the url
  let cart_count = document.querySelector("#cart_count_number").innerText;
  let cart_data = document.querySelector("#cart_data").innerText;

  document.querySelectorAll(".nav_item").forEach(function(link){
    link.addEventListener('click', function(e){
      e.preventDefault();
      let element = document.querySelector(`#${this.id.split("_")[0]}`);
      element.scrollIntoView();
    });
  });
  place_order_button_state();
  purchase_confirm();
  // Get csrf token
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

  function place_order_button_state(){
    if (Number(cart_count)){
      document.querySelector("#place_order_button").disabled = false;
    }
    else{
      document.querySelector("#place_order_button").disabled = true;
    }
  }
  function purchase_confirm(){
    let button = document.querySelector("#purchase_confirm_button");
    button.addEventListener("click", function(){
      url = "/order";
      callback = function(result){
        console.log(result);
        console.log("Purchase confirmed");
        // redirect to index page
        location.replace("/");
      }
      data = {};
      post_request(url, callback, data);
    });
  }
});
