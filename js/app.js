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
          $('.bottle-identity .bottle-code').text(bottle_tuple.bottle_code);
          $('.bottle-identity .enclosure-signature').text(bottle_tuple.enclosure_signature);
          $('.bottle-identity .bottle-verification-key').text(label_tuple.bottle_key);
          $('.bottle-identity .enclosure-verification-key').text(label_tuple.enclosure_key);
          $('.bottle-identity .bottle-signature').text(enclosure_tuple.bottle_signature);
          $('.bottle-identity .enclosure-code').text(enclosure_tuple.enclosure_code);
          
          $('.identity-verification .bottle-code').val(bottle_tuple.bottle_code);
          $('.identity-verification .enclosure-signature').val(bottle_tuple.enclosure_signature);
          $('.identity-verification .bottle-verification-key').val(label_tuple.bottle_key);
          $('.identity-verification .enclosure-verification-key').val(label_tuple.enclosure_key);
          $('.identity-verification .bottle-signature').val(enclosure_tuple.bottle_signature);
          $('.identity-verification .enclosure-code').val(enclosure_tuple.enclosure_code);
                    
          // Calculate fingerprint in browser
          var fingerprintPromise = crypto.subtle.digest({name : "SHA-256"}, decodeToUint8Array(bottle_tuple.bottle_code + enclosure_tuple.enclosure_code)).then(function(result){
            console.log("Fingerprint: " + result);
                $('.bottle-identity .fingerprint').text(result);
            }, function(reason){
              console.log("Error calculating Fingerprint: " + reason);
              $('.bottle-identity .fingerprint').text("Error calculating Fingerprint");
              
            });
          
          
          
          // Validate Identity in browser
          //var curve = sjcl.ecc.curves.c192;
          //var public_key_point = new sjcl.ecc.point( curve, label_tuple.bottle_key.x, label_tuple.bottle_key.y);
          //var public_key = new sjcl.ecc.ecdsa.publicKey(sjcl.ecc.curves.c192, public_key_point);
          //var enclosure_signature_verified = public_key.verify(decode(bottle_tuple.bottle_code), decode(enclosure_tuple.bottle_signature));
          //console.log(enclosure_signature_verified);
        }
      });
    });
};

$(document).ready(main);