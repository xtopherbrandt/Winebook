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
          var identity = JSON.parse(data);
          var bottle_tuple = identity.bottle_tuple;
          $('.bottle-codes').show();
          $('<li>').text(bottle_tuple.bottle_code).appendTo('.bottle-components' );
          $('<li>').text(bottle_tuple.enclosure_signature).appendTo('.bottle-components' );
          $('.label-codes').show();
          $('<li>').text(bottle_tuple.bottle_code).appendTo('.label-components' );
          $('<li>').text(bottle_tuple.enclosure_signature).appendTo('.label-components' );
          $('.enclosure-codes').show();
          $('<li>').text(bottle_tuple.bottle_code).appendTo('.enclosure-components' );
          $('<li>').text(bottle_tuple.enclosure_signature).appendTo('.enclosure-components' );
        }
      });
    });
};

$(document).ready(main);