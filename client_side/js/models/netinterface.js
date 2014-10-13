


App.NetInterface = DS.Model.extend({
    name: DS.attr('string'),
    inetAddr: DS.attr('string'),
    flags: DS.attr('string'),
    dstAddr: DS.attr('string'),

    receiveBytes: DS.attr('number'),
    receivePackets: DS.attr('number'),
    receiveErrs: DS.attr('number'),
    receiveDrops: DS.attr('number'),
    receiveFifo: DS.attr('number'),
    receiveFrame: DS.attr('number'),
    receiveCompressed: DS.attr('number'),
    receiveMulticast: DS.attr('number'),

    transmitBytes: DS.attr('number'),
    transmitPackets: DS.attr('number'),
    transmitErrs: DS.attr('number'),
    transmitDrops: DS.attr('number'),
    transmitFifo: DS.attr('number'),
    transmitColls: DS.attr('number'),
    transmitCarrier: DS.attr('number'),
    transmitCompressed: DS.attr('number')
});

//App.NetInterface.FIXTURES = [
//    {
//        id: 1,
//        title: 'eth0',
//        ip: '192.168.1.128'
//    },
//    {
//        id: 2,
//        title: 'wlan0',
//        ip: '192.168.2.1'
//    },
//    {
//        id: 3,
//        title: 'lo',
//        ip: '127.0.0.1'
//    }
//]