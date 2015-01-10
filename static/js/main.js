
var tetry = {
    init: function(){
        $( "#tetry-commands-content" ).load( "/tetry/api/1.0/tasks/moves" );
        tetry.add_event_handlers();
    },

    add_event_handlers: function(){
        $( ".tetry-command-group" ).each( function() {
            $(this).click(tetry.load_command_group());
         });
        $( ".tetry-command" ).each( function() {
            $(this).click(tetry.send_command());
         });
    },

    load_command_group: function(){
        $( "#tetry-commands-content" ).load( "/tetry/api/1.0/tasks/"+ $(this).attr("data") );
        $( ".tetry-command-group" ).parent().attr("class", "");
        $( this ).parent().attr("class", "active");
        tetry.add_event_handlers();
    },

    send_command: function(){
        tetry.ajaxer("/tetry/api/1.0/tasks/", {name: $(this).text()});
    },

    ajaxer: function(url, data){
        $.ajax({
            url: "post.php",
            data: data,
            type: "POST",
            dataType : "json",
            success: function( json ) {
                alert( json.status );
            },
            error: function( xhr, status, errorThrown ) {
                alert( "Sorry, there was a problem!" );
                console.log( "Error: " + errorThrown );
                console.log( "Status: " + status );
                console.dir( xhr );
            },

            // Code to run regardless of success or failure
            complete: function( xhr, status ) {
                //alert( "The request is complete!" );
            }
        });
    }
};

$(function() {
    tetry.init();
});
