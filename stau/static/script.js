var chart;
var d;
$(function(){


    $('#variant').change(function (e) {
        var variant = $("#variant option:selected").attr('value')
        $.getJSON('var/'+variant.split('v')[1]).success(function(data){
            chart = time_response({data:data.data,name:'test'});
            chart.render()
        });
    });

    $('#clear').click(function (e) {
        var variant = $("#variant option:selected").attr('value')
        $.getJSON('var/'+variant.split('v')[1]+'/clear').success(function(data){
            chart = time_response({data:data.data,name:'test'});
            chart.render()
        });
    });

    $('#simou').click(function (e) {
        var variant = $("#variant option:selected").attr('value')
        $.getJSON('var/'+variant.split('v')[1]+'/simou').success(function(data){
            d = data;
            chart = time_response({data:data.data,name:'test'});
            chart.render()
            $(_.template($('#tf-template').html(),data)).appendTo('#tf')
            MathJax.Hub.Typeset()
        });
    });



})