var chart;
var d;
$(function(){
    $('#variant').change(function (e) {
        var variant = $("#variant option:selected").attr('value')
        $.getJSON('var/'+variant).success(function(data){
            chart = time_response({data:data.data,name:'test'});
            chart.render()
        });
    });

    $('#clear').click(function (e) {
        var variant = $("#variant option:selected").attr('value')
        $.getJSON('var/'+variant+'/clear').success(function(data){
            chart = time_response({data:data.data,name:'test'});
            chart.render()
        });
    });

    $('#simou').click(function (e) {
        var variant = $("#variant option:selected").attr('value')
        $.getJSON('var/'+variant+'/simou').success(function(data){
            d = data;
            chart = time_response({data:data.data,name:'test'});
            chart.render()
            $('#tf').html(_.template($('#tf-template').html(),data))
            MathJax.Hub.Typeset()
        });
    });
});