/* ----- AUTOMATIC TRANSLATION FUNCTIONS -------- */

function automatic_translation(div_id){
    // Get language_inputs
    var AT_LANGUAGE_PRIORITY = at_language_priority;
    var empty_inputs = [];
    var useful_inputs = [];
    var useful_inputs_id = [];
    var inputs = $(div_id).find('input, textarea');
    inputs.each(function(index, element){
        if ($(this).val() != ""){
            useful_inputs.push($(this));
            useful_inputs_id.push($(this).attr("id"));
        }
        else{
            empty_inputs.push($(this));
        }
    });
    if (useful_inputs.length != 0){ // Minimun input check
        var useful_id;
        var exit;
        $.each(AT_LANGUAGE_PRIORITY,function(index, element){            
            if (exit)
                return false;
            var language = element;
            exit = false;
            $.each(useful_inputs_id,function(index, element){
                if (element.toLowerCase().indexOf("_"+language+"-") >= 0){
                    useful_id = element;
                    exit = true;
                    return false;
                }  
            
            });
        });
        
    useful_input = $("#"+useful_id);
    source_language = $("#"+useful_id).attr("id").split('-')[0].split('_')[2];
    $.each(empty_inputs, function(index, element){
        // TODO: HAU HOBETU! Bete falta diren hizkuntzak azpiko funtzioari deituz
        try{
            target_language = $(this).attr("id").split('-')[0].split('_')[2];
            opentrad_automatic_translation($(useful_input).attr("id"),$(this).attr("id"),source_language, target_language);
        }
        catch(ex){
            console.log(ex);
        }
    });
                
    }
    else{ // No input!?
        alert("All inputs are empty!");
        return false;
    }
}


function opentrad_automatic_translation(source_input_id, target_input_id, source_lang, target_lang){
    var translated_text;
    var text_to_translate = $("#"+source_input_id).val();
    /*$.ajax({
           url: "http://api.opentrad.com/translate.php",
           dataType: "text",
           crossDomain: true,
           data: { text: text_to_translate, lang: source_lang+'-'+target_lang, cod_client : opentrad_code},
           success : function(data, status, xhr){
           
               translated_text = data;  
               if (translated_text.indexOf("Error: Mode ") < 0){ // The translation has no errors             
                $("#"+target_input_id).val(translated_text);
               }
               else{
                console.log(translated_text);
               }
               
           
           },
           error: function(jqXHR, textStatus, errorThrown) {        
            }
    });
    */
    var xhr = createCORSRequest('GET', "http://api.opentrad.com/translate.php?text="+text_to_translate+"&lang="+source_lang+'-'+target_lang+"&cod_client="+opentrad_code);
    if (!xhr) {
        alert('CORS not supported');
        return;
    
  }
  // Response handlers.
  xhr.onload = function() {
    translated_text = xhr.responseText;  
    if (translated_text.indexOf("Error: Mode ") < 0){ // The translation has no errors             
        $("#"+target_input_id).val(translated_text);
    }
    else{
        console.log(translated_text);
    }
  };

  xhr.onerror = function() {
    alert('Woops, there was an error making the request.');
  };

  xhr.send();

}

function createCORSRequest(method, url) {
  var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {

    // Check if the XMLHttpRequest object has a "withCredentials" property.
    // "withCredentials" only exists on XMLHTTPRequest2 objects.
    xhr.open(method, url, true);

  } else if (typeof XDomainRequest != "undefined") {

    // Otherwise, check if XDomainRequest.
    // XDomainRequest only exists in IE, and is IE's way of making CORS requests.
    xhr = new XDomainRequest();
    xhr.open(method, url);

  } else {

    // Otherwise, CORS is not supported by the browser.
    xhr = null;

  }
  return xhr;
}
/*-------------------------------------------------*/
