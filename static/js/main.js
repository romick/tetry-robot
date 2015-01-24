
var tetry = {
    init: function(){
        $( "#tetry-commands-content" ).load( "/tetry/api/1.0/tasks/moves" );
        tetry.add_event_handlers();
        $('.log-container').slimScroll({
            height: '150px'
        });

        //wheel size 100x100
        $('.wheel').drawArc({
            layer: true,
            fillStyle: 'black',
            x: 100, y: 100,
            radius: 90,
            click: tetry.send_command_from_wheel,
            mousemove: tetry.draw_line_on_wheel
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
        tetry.ajaxer("/tetry/api/1.0/tasks/", { name: element.text(),
                                                command: element.attr("command"),
                                                data: element.attr("data")});
//        tetry.log_update();
    },

    send_command_from_wheel: function (layer) {
                //TODO: change from hard-coded to calculated
                var x = layer.eventX - 100;
                var y = layer.eventY - 100;
                var angle = tetry.coords2angle(x, y);
                var command = $(this).attr("command")
                tetry.ajaxer("/tetry/api/1.0/tasks/", {name: "wheel", command: command, data: angle});
    },

    coords2angle: function (x, y) {
        var angle = Math.atan2(y, x)/Math.PI*180;
        angle = angle + 90;
        if (angle < 0){
            angle = 360 + angle;
        };
        return angle;

    },

    draw_line_on_wheel: function (layer) {
        var angle = tetry.coords2angle(layer.eventY, layer.eventX)
        var length = Math.sqrt((layer.eventX-50)*(layer.eventX-50)+(layer.eventY-50)*(layer.eventY-50))
        $(this).drawLine ({
            strokeStyle: "white",
            strokeWidth: 2,
            x1: 100,
            y1: 100,
            x2: layer.eventX,
            y2: layer.eventY

        });
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
                tetry.log_update();
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
