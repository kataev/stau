/**
 * Created by PyCharm.
 * User: bteam
 * Date: 11.01.12
 * Time: 13:05
 * To change this template use File | Settings | File Templates.
 */
time_response = function (args) {
    chart = new Highcharts.Chart({
        chart:{ renderTo:args.node || 'chartNode',
            defaultSeriesType:'line'
            ,zoomType:'x'
//        ,type:'scatter'
        },
        exporting:{enabled:true},
        buttons:{
            exportButton:{enabled:false}
        },
        title:{text:null, x:0, floating:true},
//    series:[ {name:name,data:args.step} ],
        xAxis:{title:{text:null},
            title:{ text:null },
            startOnTick:false,
            endOnTick:false,
            minorTickInterval:'auto',
            lineColor:'#000',
            lineWidth:1,
            tickWidth:1,
            tickColor:'#010'
        },
        yAxis:{
            title:{ text:null },
            startOnTick:false,
            endOnTick:false,
            minorTickInterval:'auto',
            lineColor:'#000',
            lineWidth:1,
            tickWidth:1,
            tickColor:'#000'
        },
        credits:{enabled:false}
//    ,tooltip: {
//        formatter: function() {
//            return '<b>'+ this.series.name+ ':</b> <i>'+ this.y +'</i><br/>'
//
//        }}
    });

    Highcharts.setOptions({
        lang: {
            resetZoom:'Сбросить зум'
        }
    });

    return chart
}