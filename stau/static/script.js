$(function(){


    $('#variant').change(function (e) {
        var variant = $("#variant option:selected").attr('value')
        $.getJSON('var/'+variant.split('v')[1]).success(function(data){
            console.log(data)
        })
    })

})