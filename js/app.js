var main = function ()
{
  //Enroll button click handler
  $('#enroll-btn').click(function()
    {
      $.ajax(
      {
        type: 'POST',
        url: "/enroll_bottle",
        data: 
        {
          vintage: $('#vintage').val(),
          producer: $('#producer').val(),
          name: $('#name').val()
        },
        success: function( data ) 
        {
          $( "#weather-temp" ).html( "<strong>" + data + "</strong> degrees" );
        }
      });
    });
};

$(document).ready(main);