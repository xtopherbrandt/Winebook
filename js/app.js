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
          var label_tuple = identity.label_tuple;
          var enclosure_tuple = identity.enclosure_tuple;
          $('<p>').text(bottle_tuple.bottle_code).addClass('code').appendTo('.bottle-code');
          $('<p>').text(bottle_tuple.enclosure_signature).addClass('code').appendTo('.enclosure-signature');
          $('<p>').text(label_tuple.bottle_key).addClass('code').appendTo('.bottle-verification-key');
          $('<p>').text(label_tuple.enclosure_key).addClass('code').appendTo('.enclosure-verification-key');
          $('<p>').text(enclosure_tuple.bottle_signature).addClass('code').appendTo('.bottle-signature');
          $('<p>').text(enclosure_tuple.enclosure_code).addClass('code').appendTo('.enclosure-code');
        }
      });
    });
};

$(document).ready(main);