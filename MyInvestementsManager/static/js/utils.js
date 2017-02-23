 function loadBody(url) {
    	$.get( url, function( data ) {
    		  $( "#pageBody" ).html( data);
    		});
    };
   