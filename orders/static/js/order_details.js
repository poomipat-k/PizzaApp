document.addEventListener('DOMContentLoaded', function(){
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

  // Initialize parameter for send ajax request
  let order_id = document.querySelector("#order_id").innerText;
  let url = "/change_order_status";
  let action = function(result){
    console.log(result);
    location.replace("/order_view")
  };
  let data;

  // Listen on click event
  document.addEventListener("click", e => {

    if (e.target.id == "complete_button"){
      console.log(e.target.id + " clicked");

      data = {
        "order_id" : order_id,
        "status" : "complete"
      };
      // Send AJAX POST request
      $.ajax({
        url : url,
        success : action,
        type : "POST",
        data : data
      });
    }
    else if (e.target.id == "pending_button"){
      console.log(e.target.id + " clicked");
      data = {
        "order_id" : order_id,
        "status" : "pending"
      };
      // Send AJAX POST request
      $.ajax({
        url : url,
        success : action,
        type : "POST",
        data : data
      });
    }

  });
});
