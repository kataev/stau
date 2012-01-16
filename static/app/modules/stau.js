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

    })

    Stau.Transfer = Backbone.Model.extend({
        initialize:function () {
            this.order = 0;
            this.bind('change', this.set_order, this);
            this.href = '#transfer/'
        },
        defaults:{
            'step_length':300,
            'title':'Передаточная функция'
        },
        urlRoot:'/api/transfer',
        set_order:function () {
            this.order = this.get('den') ? _.max([this.get('den').length, this.get('num').length]) - 1 : 0;
        }
    });

    Stau.Transfer_simp = Backbone.Model.extend({
        initialize:function () {

        },
        defaults:{
            'title':'Передаточная функция'
        },
        urlRoot:'/api/transfer_simp'
    });

    Stau.Response = Backbone.Model.extend({
        urlRoot:'/api/response',
        initialize:function () {
            r = this;
            this.href = '#response'
        },
        defaults:{
            'title':'Динамическая характеристика'
        },
        simou:function () {
            var tf = new Stau.Transfer
            $.ajax({url:this.url() + '/simou/', dataType:'json', context:this}).success(function (data) {
                tf.set(data)
            });
            return tf
        },
        tangent:function () {
            var tf = new Stau.Transfer_simp
            $.ajax({url:this.url() + '/tangent', dataType:'json', context:this}).success(function (data) {
                tf.set(data)
            });
            return tf
        },
        match3:function () {
            var tf = new Stau.Transfer_simp
            $.ajax({url:this.url() + '/match3', dataType:'json', context:this}).success(function (data) {
                tf.set(data)
            });
            return tf
        },
        norm:function () {
            $.ajax({url:this.url() + '/normalization', dataType:'json', context:this}).success(function (data) {
                this.set(data)
            });
        },
        flat:function (flat) {
            $.ajax({url:this.url() + '/flattening/' + flat, dataType:'json', context:this}).success(function (data) {
                this.set(data)
            });
        },
        line:function () {
            $.ajax({url:this.url() + '/linearization', dataType:'json', context:this}).success(function (data) {
                this.set(data)
            });
        }
    });

    Stau.Collection = Backbone.Collection.extend({
        model:Stau.Transfer,
        url:'/api/transfer'
    });
    Stau.Router = Backbone.Router.extend({
        routes:{
            "transfer/:id":"transfer"
        },
        transfer:function (id) {
            var model = Stau.transfer_col.at(id);
            var view = new Stau.Views.Transfer({model:model});
            $(view.el).appendTo('#container')
            view.render(function(){})

        }
    });


    Stau.Views.View = Backbone.View.extend({
        tagName:'div',
        className:'span16 response',
        step:function () {
            if (this.model.chart) {
                this.model.chart.remove()
            }
            $.ajax({url:this.model.url() + '/step', dataType:'json', context:this, data:{length:this.$(".length").attr('value')}})
                .success(function (data) {
                    if (data.error) {
                        alert(data.message)
                    }
                    else {
                        this.model.set({time:data.time, step:data.data});
                        var data = this.model.get('step');
                        var time = this.model.get('time');
                        var series = _.zip(time, data);
                        this.model.chart = chart.addSeries({data:series, name:this.model.get('title'), marker:{ enabled:false },
                            allowPointSelect:true, id:'transfer' + this.model.get('id')});
                        $(this.el).css('background-color', this.model.chart.color);
                    }
                });
        },
        del_chart:function () {
            if (this.model.chart) {
                this.model.chart.remove()
            }
        },
        math_end_render:function () {
            console.log('math rendered')
        }
    });

    Stau.Views.Menu = Backbone.View.extend({
        initialize:function(){
            this.model.menu = this;
        },
        tagName:'div',
        className:'span4',
        template:"/static/app/templates/sidebar.html",
        events: {
            'click .step':'step',
            'click .open':'open'
        },
        render:function(){
            namespace.fetchTemplate(this.template, function (tmpl) {
                var data = this.model.toJSON();
                data.href = this.model.href
                $(this.el).html(tmpl(data));
                this.$('[rel="popover"]').popover({html:true})
            }, this);
        },
        step:function () {
            if (this.model.chart) {
                this.model.chart.remove()
            }
            console.log(this.model.step_len)
            $.ajax({url:this.model.url() + '/step', dataType:'json', context:this, data:{length:this.model.get('step_length')}})
                .success(function (data) {
                    if (data.error) {
                        alert(data.message)
                    }
                    else {
                        this.model.set({time:data.time, step:data.data});
                        var data = this.model.get('step');
                        var time = this.model.get('time');
                        var series = _.zip(time, data);
                        this.model.chart = chart.addSeries({data:series, name:this.model.get('title'), marker:{ enabled:false },
                            allowPointSelect:true, id:'transfer' + this.model.get('id')});
                        $(this.el).css('background-color', this.model.chart.color);
                    }
                });
        },
        open:function(){

        }
    })


    Stau.Views.Response = Stau.Views.View.extend({
        template:"/static/app/templates/sidebar.html",
        events:{
            "click .simou":"simou",
            "click .norm":"norm",
            "click .flat":"flat",
            "click .line":"line",
            "click .tangent":"tangent",
            "click .match3":"match3",
            "click .step":"step",
            "change .length":'set_length'
        },
        render:function () {
            namespace.fetchTemplate(this.template, function (tmpl) {
                var data = this.model.toJSON();
                data.tf = {num:['a','a','a'],den:['a','a','a']}
                $(this.el).html(tmpl(data));
                this.$('[rel="popover"]').popover({html:true})
            }, this);
        },
        step:function () {
            if (this.model.chart) {
                this.model.chart.remove()
                this.model.chart = null;
                return;
            }
            var d = this.model.toJSON()
            var series = _.zip(d.time, d.data);
            this.model.chart = chart.addSeries({data:series, name:'Динамическая характеристика ' + d.id,
                marker:{ enabled:false }, allowPointSelect:true, id:'response' + d.id});
//            $(this.el).css('background-color', this.model.chart.color);
        },
        simou:function () {
            var tf = this.model.simou()
            var view = new Stau.Views.Transfer({model:tf});
            $(view.el).appendTo('#container')
            view.render()
            tf.fetch()
        },
        tangent:function () {
            var tf = this.model.tangent()
            var view = new Stau.Views.Transfer_simp({model:tf});
            $(view.el).appendTo('#container')
            view.render()
            tf.fetch()
        },
        match3:function () {
            var tf = this.model.match3()
            var view = new Stau.Views.Transfer_simp({model:tf});
            $(view.el).appendTo('#container')
            view.render()
            tf.fetch()
        },
        flat:function () {
            var flat = this.$('input.flat').attr('value');
            this.model.flat(flat);
        },
        line:function () {
            this.model.line();
        },
        norm:function () {
            this.model.norm()
        },
        set_length:function(){
            console.log(this.$('.length').attr('value'))
        }
    });

//    Stau.Views.Response.prototype = Stau.Views.View;

    Stau.Views.Transfer_simp = Stau.Views.View.extend({
        initialize:function () {
            this.model.bind('change:t', this.render, this);
            this.model.bind('change:tau', this.render, this);
            this.model.view = this;
        },
        template:"/static/app/templates/transfer_s.html",
        events:{
            "click .step":"step",
            "click .chart_del":"del_chart"
        },
        render:function (done) {
            namespace.fetchTemplate(this.template, function (tmpl) {
                var data = this.model.toJSON();
                $(this.el).html(tmpl({tf:data}));
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, this.$('.math').attr('id'), this.math_end_render]);
            }, this);
        }
    })

    Stau.Views.Transfer = Stau.Views.View.extend({
        initialize:function () {
            this.model.bind('change:num', this.render, this);
            this.model.bind('change:den', this.render, this);
            this.model.view = this;
            m = this.model;
            this.model.bind(this.set_length)
        },
        template:"/static/app/templates/transfer.html",
        events:{
            "click .simp":"simplification",
            "click .step":"step",
            "click .nyquist":"nyquist",
            "dblclick .math":"edit",

            "click .chart_del":"del_chart",
            "click .remove":"remove"
        },
        render:function (done) {
            // Fetch the template, render it to the View element and call done.
            namespace.fetchTemplate(this.template, function (tmpl) {
                var data = this.model.toJSON();
                data.order = data.den ? _.max([data.den.length, data.num.length]) - 1 : 0;
                $(this.el).html(tmpl({tf:data}));
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, this.$('.math').attr('id'), this.math_end_render]);
                this.$('[rel="twipsy"]').twipsy()
                this.$('.length').change($.proxy(function(e){
                    this.model.set('step_length') = $(e.target).attr('value');
                },this));
            }, this);
        },
        simplification:function () {
            var tf = new Stau.Transfer
            var view = new Stau.Views.Transfer({model:tf});
            $(view.el).appendTo('#container')
            view.render()
            $.ajax({url:this.model.url() + '/simp/' + this.$('.order').attr('value'), dataType:'json', context:this}).success(function (data) {
                tf.set(data)
            })
        },
        nyquist:function () {
            $.ajax({url:this.model.url() + '/nyquist', dataType:'json', context:this})
                .success(function (data) {
                    if (data.error) {
                        alert(data.message)
                    }
                    else {
                        var n = _.zip(data.a, data.b)
                        chart.addSeries({data:n, marker:{ enabled:true }, stack:1 });
                    }
                })
        },
        edit:function () {

        }
    });

    // This will fetch the tutorial template and render it.
    Stau.Views.Tutorial = Backbone.View.extend({
        template:"/static/app/templates/example.html",
        render:function (done) {
            time_response({})
            Stau.transfer_col = new Stau.Collection;
            Stau.transfer_col.fetch().success(function (data) {
                Stau.transfer_col.each(function (model) {
                    var view = new Stau.Views.Menu({model:model});
                    $(view.el).appendTo('#sidebar')
                    view.render()
//                    model.fetch()
                });
            })
//            var r = new Stau.Response({id:1})
//            v = new Stau.Views.Response({model:r})
//            r.fetch()
//            v.render()
//            $(v.el).appendTo('#sidebar')

//            s = new Stau.Transfer_simp({id:1})
//            e = new Stau.Views.Transfer_simp({model:s})
//            s.fetch()
//            e.render()
//            $(e.el).appendTo('#container')
        }
    });


})(namespace.module("stau"));
