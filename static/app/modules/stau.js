// Use an IIFE...
// (http://benalman.com/news/2010/11/immediately-invoked-function-expression/)
// to assign your module reference to a local variable, in this case Example.
//
// Change line 16 'Example' to the name of your module, and change line 38 to
// the lowercase version of your module name.  Then change the namespace
// for all the Models/Collections/Views/Routers to use your module name.
//
// For example: Renaming this to use the module name: Project
//
// Line 16: (function(Project) {
// Line 38: })(namespace.module("project"));
//
// Line 18: Project.Model = Backbone.Model.extend({
//
(function (Stau) {

    Stau.Model = Backbone.Model.extend({
        defaults: {
            "num":  [1,2],
            "den":  [2,3]
        },
        urlRoot:'/transfer'
    });
    Stau.Collection = Backbone.Collection.extend({ /* ... */ });
    Stau.Router = Backbone.Router.extend({
        routes:{
            "transfer/:id":"transfer"
        },
        transfer:function (id) {
            var tf = new Stau.Model({id:id});
            var view = new Stau.Views.Transfer({model:tf});
            view.el = $('<div></div>').appendTo('body')
            view.render()
            tf.fetch()

//            $.getJSON(m.url()+'/step').success(function(d){time_response({data:d})})

        }
    });

    Stau.Views.Transfer = Backbone.View.extend({
        initialize:function(){
            this.model.bind('change',this.render,this);
            m = this.model;
        },
        template:"/static/app/templates/transfer.html",
        tagName:'div',
        events: {
            "click .simp" : "s"
        },
        render:function (done) {
            // Fetch the template, render it to the View element and call done.
            namespace.fetchTemplate(this.template, function (tmpl) {
                $(this.el).html(tmpl({tf:this.model.toJSON()}));
                MathJax.Hub.Typeset()
            },this);
        },
        s:function(){
            console.log(e)
        }
    });

    // This will fetch the tutorial template and render it.
    Stau.Views.Tutorial = Backbone.View.extend({
        template:"/static/app/templates/example.html",

        render:function (done) {
            var view = this;

            // Fetch the template, render it to the View element and call done.
            namespace.fetchTemplate(this.template, function (tmpl) {
                view.el.innerHTML = tmpl();

                done(view.el);
            });
        }
    });


})(namespace.module("stau"));
