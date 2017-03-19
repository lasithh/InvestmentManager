    
function loadDataToContainer(url, parameters, containerId) {
    $.get( url, parameters, function( data ) {
    		 $( "#" + containerId).html( data);
    });
 } 


function loadBody(url) {
    	/*$.get( url, function( data ) {
    		  $( "#pageBody" ).html( data);
    		});*/
    	
    	loadDataToContainer(url, "", "pageBody");
 }
    
    
  
   