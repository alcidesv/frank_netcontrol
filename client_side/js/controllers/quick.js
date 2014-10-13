
function Quick_runAction(action) {
    var ws = new WebSocket(this.get('baseUrl'));
    this.set('block', true);
    var self = this;

    ws.onopen = function () {
        // Ask the server to start streaming the log
        var connect_petition = {
            'action': action,
            'max-time': self.get('connectTime')
        };
        ws.send(JSON.stringify(connect_petition));
    };
    ws.onmessage = function (e) {
        // Just publish the messages
        var data = JSON.parse(e.data);
        var logOutput = self.get('logOutput');
        if (data.type == 'update-log') {
            logOutput.pushObject(data.output);
        } else if (data.type == 'update-state') {
            var model = self.get('model');
            model.reload();
            ws.close();
            if (data.hint === action) {
                logOutput.pushObject('------------- ok -------------------');
                setTimeout(function () {
                        logOutput.clear();
                    },
                    10000
                )
            } else {
                // Just add a mark
                logOutput.pushObject('------------- mark -----------------');
            }
            self.set('block', false);
        }
    };
    ws.onerror = function (err) {
        console.log("Error:", err);
    }
}

App.QuickController = Ember.ObjectController.extend({
    // Initial value: wired to the typical time of connection
    connectTime: 10,

    logOutput: [],

    baseUrl: function(){
        return "ws://" + window.location.host +"/ws/connect-console/";
    }.property(),

    // Says if the buttons can be pressed
    block: false,

    setConnectionTime: function(new_conn_time)
    {
        this.set('connectTime', new_conn_time);
    },

    transStateNow:function(){
        var raw_prop = this.get('stateNow');
        switch (raw_prop)
        {
            case 'connected':
                return 'Módem conectado/teléfono ocupado por módem';
            case 'disconnected':
                return 'Teléfono libre/Módem desconectado';
        }
        return raw_prop;
    }.property('stateNow'),

    connectLabelClass: function(){
        var raw_prop = this.get('stateNow');
        switch (raw_prop)
        {
            case 'connected':
                return 'label-connected';
            case 'disconnected':
                return 'label-disconnected';
        }
        return raw_prop;
    }.property('stateNow'),



    initConnect: function(){
        console.log("initConnect");
        var action = 'connect';


        Quick_runAction.call(this, action);
    },

    extendConnect: function() {
        console.log("ExtendConect");
    },

    initDisconnect: function(){
        console.log("initDisconnect");
        var action = 'disconnect';


        Quick_runAction.call(this, action);
    },

    hasLog: function() {
        var logOutput = this.get('logOutput');
        return logOutput.length > 0;
    }.property('logOutput.@each')


});

