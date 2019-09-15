function remove_all_classes()
{
  var classList = document.getElementById('icon').className.split(/\s+/);

    for (var i = 0; i < classList.length; i++) 
    {
      $("#icon").removeClass(classList[i]);
    }
}
  
function change_icon( condition_code )
{
  var hour = (new Date).getHours();
  //thunderstorm
  if( condition_code >= 200 && condition_code <= 232 )
  {
    remove_all_classes();
    $("#icon").addClass("fas fa-bolt");
  }
  else if( condition_code >= 300 && condition_code <= 321 )
  {
    remove_all_classes();

    if( hour >= 6 && hour <= 20 )
    {
      $("#icon").addClass("fas fa-cloud-rain");
    }
    else
    {
      $("#icon").addClass("fas fa-cloud-moon-rain");
    }
  }
  else if( condition_code >= 500 && condition_code <= 531 )
  {
    remove_all_classes();
    $("#icon").addClass("fas fa-cloud-showers-heavy");
  }
  else if( condition_code >= 600 && condition_code <= 622 )
  {
    remove_all_classes();
    $("#icon").addClass("far fa-snowflake");
  }
  else if( condition_code >= 701 && condition_code <= 781 )
  {
    remove_all_classes();
    $("#icon").addClass("fas fa-wind");
  }
  else if( condition_code == 800 )
  {
    remove_all_classes();

    if( hour >= 6 && hour <= 20 )
    {
      $("#icon").addClass("far fa-sun");
    }
    else
    {
      $("#icon").addClass("far fa-moon");
    }
  }
  else if( condition_code >= 801 && condition_code <= 804 )
  {
    remove_all_classes();

    if( hour >= 6 && hour <= 20 )
    {
      $("#icon").addClass("fas fa-cloud");
    }
    else
    {
      $("#icon").addClass("fas fa-cloud-moon")
    }
  }
  else
  {
    remove_all_classes();
  }
}
    
$(document).ready(function(){

  $('form').on('submit',function(){

    $.ajax({

        data : { city_input : $("#city_input").val() },
        type: 'POST',
        url: '/weather_today'

    }).done(function(data){

        if(data.response == '404')
        {
            remove_all_classes();
            $('#city').text(data.city);
            $("#city").css("left","15%");
            $('#description').text("");
            $('#t_min').text("");
            $('#t_max').text("");
              
        }
        else
        {
            change_icon(data.condition_code);
            $('#city').text(data.city);
            $('#description').text(data.weather_description);
            $('#t_min').text(data.weather_temp_min + "°C" );
            $('#t_max').text(data.weather_temp_max + "°C");
        }
      });
    event.preventDefault();
  });
});