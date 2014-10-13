App.DocumentationNode = DS.Model.extend({
    mdName: DS.attr('string'),
    documentationText: DS.belongsTo('App.DocumentationText')
});

App.DocumentationText = DS.Model.extend({
    mdText: DS.attr('string'),
    documentationNode: DS.belongsTo('App.DocumentationNode'),
    html: function()
    {
        var md = this.get("mdText");
        if (md==undefined)
            md = "No text here";

        var tree = markdown.parse(md);
        var refs = {};
        if ( Array.isArray(tree[1]))
        {
            // Force-feed the attributes.
            refs = {};
            tree.splice(1,0,{'references': refs});
        } else
        {
            refs = tree[1].references;
        }


        ( function find_link_refs( jsonml ) {
            if ( jsonml[ 0 ] === "link_ref" ) {
                var ref = jsonml[ 1 ].ref;

                // if there's no reference, define a wiki link
                if ( !refs[ ref ] ) {
                    if ( ref.search(/\.\d/)>0)
                    {
                        refs[ ref ] = {
                            href: "#/documentation-nodes/viewman/" + ref.replace(/\s+/, "" )
                        };
                    }
                    else{
                        refs[ ref ] = {
                            href: "#/documentation-nodes/viewdoc/" + jsonml[2].replace(/\s+/, "" )
                        };
                    }
                }
            }
            else
            {
                jsonml.forEach( function(x){
                    if (Array.isArray(x))
                    {
                        find_link_refs(x);
                    }
                });
            }
        } )( tree );

// convert the tree into html
        var html = markdown.renderJsonML( markdown.toHTMLTree( tree ) );
        var result = html;


        //var result = markdown.toHTML(md);
        result.htmlSafe();
        return result;
    }.property('mdText')
});

App.ManPage = DS.Model.extend({
    htmlized : DS.attr('string'),
    title: DS.attr('string'),
    section: DS.attr('number'),
    unescaped: function()
    {
        var res = this.get("htmlized");
        res.htmlSafe();
        return res;
    }.property("html")
});