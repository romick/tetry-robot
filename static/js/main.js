
var tetry = {
    init: function(){
        $( "#tetry-commands-content" ).load( "/tetry/api/1.0/tasks/moves" );
        tetry.add_event_handlers();
    },

    add_event_handlers: function(){
        $("body").delegate( ".tetry-command-group", "click", function() {
            tetry.load_command_group($(this));
         });
        $("body").delegate( ".tetry-command", "click", function() {
            tetry.send_command($(this).text());
         });
    },

    load_command_group: function(element){
        $( "#tetry-commands-content" ).load( "/tetry/api/1.0/tasks/"+ element.attr("data") );
        $( ".tetry-command-group" ).parent().attr("class", "");
        element.parent().attr("class", "active");
        //tetry.add_event_handlers();
    },

    send_command: function(text){
        tetry.ajaxer("/tetry/api/1.0/tasks/", {name: text});
    },

    ajaxer: function(url, data){
        console.log(data);
        $.ajax({
            url: url,
            contentType: 'application/json',
            data: JSON.stringify(data),
            type: "POST",
            dataType : "json",
            success: function( json ) {
                console.log( json.status + " " + json.name);
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
    $(window).ajaxError(function(evt, evtData) {
        if(evtData && ('responseText' in evtData)) {
          var debuggerWindow = window.open('about:blank', 'debuggerWindow');
          debuggerWindow.document.open();
          debuggerWindow.document.write(evtData.responseText);
          debuggerWindow.document.close();
        }
    });
});
