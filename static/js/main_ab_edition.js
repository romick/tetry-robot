var wamp_connection = null;
var sess = null;


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

        //leg angle sliders

        if (jQuery.ui) {
            console.log("UI loaded!")
        } else {
            console.log("UI NOT LOADED!!")
        };

        $( ".leg-1 span" ).each( function (){

            $( this ).slider({
                    min:10,
                    max:100,
                    value: 40,
                    range: "min",
                    animate: true
            });

         });

        wamp_connection = new autobahn.Connection({
            url: 'ws://127.0.0.1:8080/ws',
            realm: 'realm1'
        });
        wamp_connection.onopen = function(session) {
            sess = session;
            console.log("connecting to wamp...");
            if (sess.isOpen) {
                console.log("Connected to wamp!");
            };
            sess.subscribe('com.tetry.log', tetry.on_log_receive)
        };
        wamp_connection.onclose = function(reason, details) {
            sess = null;
            console.log("connection closed ", reason);
        }

        wamp_connection.open();
    },

    add_event_handlers: function(){
        $("body").delegate( ".tetry-command", "click", function() {
            tetry.send_command($(this));
         });
    },

    on_log_receive: function(log_record){
        console.log("Got log:",log_record);
        $(".tetry-log").prepend("<tr><td>" + JSON.stringify(log_record) + "</td></tr>");
    },

    load_command_group: function(element){
        $( "#tetry-commands-content" ).load( "/tetry/api/1.0/tasks/"+ element.attr("data") );
        $( ".tetry-command-group" ).parent().attr("class", "");
        element.parent().attr("class", "active");
    },


    send_command: function(element){
        var msg = { name: element.text(),
                    command: element.attr("command"),
                    data: element.attr("data")};
        tetry.ajaxer("/tetry/api/1.0/tasks/", msg);
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
        sess.publish('com.tetry.run_command', [data], {}, {acknowledge: true, exclude_me: false}).then(
            function (publication) {
                // publish was successful
                console.log("Command published");
            },
            function (error) {
                // publish failed
                console.log("Command publishing failed");
            }
        );

    },


//    log_update: function () {
//        $.get('/tetry/api/1.0/logs/', function(json){
//            console.log(json);
//            if (json.record) {
//                $(".tetry-log").prepend("<tr><td>" + JSON.stringify(json.record) + "</td></tr>");
//            };
//            if (!json.empty){
//                tetry.log_update();
//            };
//
//        }, "json");
//    }



};

$(function() {
    tetry.init();
//    $(window).ajaxError(function(evt, evtData) {
//        if(evtData && ('responseText' in evtData)) {
//          var debuggerWindow = window.open('about:blank', 'debuggerWindow');
//          debuggerWindow.document.open();
//          debuggerWindow.document.write(evtData.responseText);
//          debuggerWindow.document.close();
//        }
//    });
//    window.setInterval(tetry.log_update, 10000);

});
