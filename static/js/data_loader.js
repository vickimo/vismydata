  $(function(){
    $.getJSON("/load", function(data) {
      console.log(data)
    });
  });