App.Router.map(function() {
    this.route('netinterfaces');
    this.route('quick');
    this.route('misc-status');
//    this.route('documentation-nodes');
    this.resource('documentation-nodes', function(){
        this.route('viewdoc', {path:"viewdoc/:documentation_node_id"});
        this.route('viewman', {path:"viewman/:man_page_id"});
    });

});

App.NetinterfacesRoute = Ember.Route.extend({
    model: function(){
        var res =App.NetInterface.find();
        return res;
    }
})

App.QuickRoute = Ember.Route.extend({

    setupController: function(controller, connection_state)
    {
        controller.set('model', connection_state);
    },

    model: function(){
        // Fetch ...
        var res = App.ConnectionState.find(1);
        return res;
    }

});

App.MiscStatusRoute = Ember.Route.extend({
    setupController: function(controller, misc_status)
    {
        controller.set('model', misc_status);
    },

    model: function(){
        // Fetch ...
        var res = App.MiscStatus.find(1);
        return res;
    }
});


App.DocumentationNodesRoute = Ember.Route.extend({
    model: function(){
        var res = App.DocumentationNode.find();
        return res;
    }
});

App.DocumentationNodesViewdocRoute = Ember.Route.extend({
    model: function( params )
    {
        var res = App.DocumentationNode.find(params.documentation_node_id);
        return res;
    }
});

App.DocumentationNodesViewmanRoute = Ember.Route.extend({
    model: function(params)
    {
        var res = App.ManPage.find(params.man_page_id);
        return res;
    }
});
