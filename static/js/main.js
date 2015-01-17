
var tetry = {
    init: function(){
        $( "#tetry-commands-content" ).load( "/tetry/api/1.0/tasks/moves" );
        tetry.add_event_handlers();
        $('.log-container').slimScroll({
            height: '150px'
        });
    },

    add_event_handlers: function(){
//        $("body").delegate( ".tetry-command-group", "click", function() {
//            tetry.load_command_group($(this));
//         });
        $("body").delegate( ".tetry-command", "click", function() {
            tetry.send_command($(this));
         });
    },

    load_command_group: function(element){
        $( "#tetry-commands-content" ).load( "/tetry/api/1.0/tasks/"+ element.attr("data") );
        $( ".tetry-command-group" ).parent().attr("class", "");
        element.parent().attr("class", "active");
        //tetry.add_event_handlers();
    },

    send_command: function(element){
        tetry.ajaxer("/tetry/api/1.0/tasks/", {name: element.text(), command: element.attr("command"), data: element.attr("data")});
        tetry.log_update();
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
    },

    log_update: function () {
        $.get('/tetry/api/1.0/logs/', function(json){
            console.log(json);
            if (json.record) {
                $(".tetry-log").prepend("<tr><td>" + JSON.stringify(json.record) + "</td></tr>");
            };
            if (!json.empty){
                tetry.log_update();
            };

        }, "json");
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
    window.setInterval(tetry.log_update, 10000);
});
