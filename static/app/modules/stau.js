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
        defaults:{
//            "num":  [1,2],
//            "den":  [2,3]
        },
        urlRoot:'/api/transfer'
    });
    Stau.Collection = Backbone.Collection.extend({
        model:Stau.Model,
        url:'/api/transfer'
    });
    Stau.Router = Backbone.Router.extend({
        routes:{
            "transfer/:id":"transfer"
        },
        transfer:function (id) {
            var tf = new Stau.Model({id:id});
            var view = new Stau.Views.Transfer({model:tf});
            $(view.el).appendTo('#container')
            view.render()
            tf.fetch()
        }
    });

    Stau.Views.TimeResponse = Backbone.View.extend({
        initialize:function(){
            this.model.bind('change:step', this.render, this);
        },
        tagName:'li',
        render:function(){
            time_response({data:this.model.get('step')});
        }
    });

    Stau.Views.Transfer = Backbone.View.extend({
        initialize:function () {
            this.model.bind('change', this.render, this);
            m = this.model;
        },
        template:"/static/app/templates/transfer.html",
        tagName:'div',
        className:'span-6',
        events:{
            "click .simp":"simp",
            "click .step":"step"
        },
        render:function (done) {
            // Fetch the template, render it to the View element and call done.
            namespace.fetchTemplate(this.template, function (tmpl) {
                $(this.el).html(tmpl({tf:this.model.toJSON()}));
                if (this.model.get('num') && this.model.get('den')) {
                    MathJax.Hub.Queue(["Typeset", MathJax.Hub, this.$('.math').attr('id'), this.math_render]);
                }
            }, this);
        },
        simp:function () {
            console.log('ololo')
        },
        step:function () {
            $.ajax({url:this.model.url() + '/step', dataType:'json', context:this})
                .success(function (data) {
                    if (data.error) {
                        alert(data.message)
                    }
                    else {
                        new Stau.Views.TimeResponse({model:this.model})
                        this.model.set({step:data});


                    }
                })
        },
        math_render:function () {
            this.math_width = this.$('.math nobr').width();
//            this.$('.math').animate({width:'200px'},function(){console.log('end animation')})
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
