//working on a function to send data asyincronously with Ajax
$(document).ready(function(){
    $('#sumbit_btn').click(function(){
      $.getJSON('/get_weather',{
        city: $('#city_input').val(),
        country: $('#country_input').val()
      },function(data){
        $('#result').text(data.city);

      });
      return false;
    });
});
//still to test and improve
