App.ConnectionState = DS.Model.extend({
    stateNow: DS.attr('string'),
    whenConnectedLast: DS.attr('date'),
    totalConnectLast30Days: DS.attr('number'),

    isConnected: function(){
        return this.get('stateNow') == 'connected';
    }                                              .property('stateNow'),

    isDisconnected: function(){
        return this.get('stateNow') == 'disconnected';
    }                                              .property('stateNow')
});